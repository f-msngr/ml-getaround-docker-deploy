# Imports
import sys
import os
import io
sys.path.append('..')

# Give access to env variables
from dotenv import load_dotenv
load_dotenv()

# Logging
import logging
logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np
import boto3
import mlflow
from mlflow.tracking import MlflowClient
import tempfile # use tmp file for joblib.dump
import joblib


# Internal
from pipeline.libs.src.utils import get_project_name
from pipeline.libs.src.aws import get_serialized_from_S3, serialize_to_s3, get_from_bucket
# Get dataset
from pipeline.core.src.load import get_cars


# sklearn imports
# Import for ColumnTransformer pipeline
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
# Metrics
from sklearn.metrics import r2_score


# --------------------------------------------------------------------------------------------------------------------------------------------------
# Apply preprocessing and get: dataset, target, features, preprocessor, X_train, X_test, Y_train, Y_test
def _apply_preprocessing()-> tuple[pd.DataFrame, str, list[str], ColumnTransformer, pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Deserialize dataset from S3 and apply ML preprocess (X/Y split, train_test_split, fit_transform)
    Returns:
    -------
    tuple:
        dataset: pd.DataFrame object in the S3 bucket
        target: target column
        features: list[str]
        preprocessor: ColumnTransformer used for target encoding (fit_transform)
        X_train, X_test, Y_train, Y_test: train_test_split output
    """
    # Import dataset
    dataset = pd.DataFrame(get_cars())
        
    logger.info(f"Deserialize object from S3: {dataset.shape}")
    
    # Split Features/Target
    target = "rental_price_per_day"
    features = [col for col in dataset.columns if col != target]
    X = dataset[features]
    Y = dataset[target]
    logger.info(f"Split Features/Target: Features: {X.shape} - Target: {Y.shape}")

    # Split data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.18, random_state=74)
    logger.info(f"Train/test split")
    
    
    #-------------------------------------------------------------------------------------------------
    # Pipeline
    #-------------------------------------------------------------------------------------------------
    # Separate features by type
    l_num_features = ["mileage", "engine_power"]
    l_cat_features = [col for col in features if col not in l_num_features]

    # Pipelines 
    # Pipeline for numeric columns
    pipeline_num_transformer = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy="mean")),
            ('scaler', StandardScaler())
            ]
        )

    # Pipeline for categorical columns
    pipeline_cat_transformer = Pipeline(
        steps=[
            ('encoder', OneHotEncoder(drop="first", handle_unknown='ignore'))
            ]
        )

    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", pipeline_num_transformer, l_num_features),
            ("cat", pipeline_cat_transformer, l_cat_features)
            ]
        )
    logger.info(f"Transformers: {preprocessor.transformers}")
    
    # Fit_transform
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)
    
    return dataset, target, features, preprocessor, X_train, X_test, Y_train, Y_test


# --------------------------------------------------------------------------------------------------------------------------------------------------
# Set up some .env variables to enable AWS connection with boto
def _setup_boto_and_mlflow_experiment():
    """ 
    This function sets some env variables with some other .env variables
    Returns:
    -------
    tuple:
        boto.client
        mlflow experiment
    """
    # Setup boto
    # Setup same AWS credentials as expected by boto credential chain
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_KEY')
    os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_REGION')  # bucket region
    logger.info(f"Load AWS credentials from .env")

    # Setup new boto session
    boto3.setup_default_session()
    # Reset new boto client
    s3 = boto3.client("s3")
    logger.info(f"Set boto session + client")


    # Setup MLflow
    # Set tracking server
    mlflow.set_tracking_uri(os.getenv('TRACKING_URI'))
    logger.info(f"Set MLFLOW_TRACKING_URI with TRACKING_URI: {os.getenv('TRACKING_URI')}")
    # Autolog
    mlflow.sklearn.autolog()

    # Set the experiment id
    experiment_name = f"{os.getenv('PROJECT_NAME')}_v2"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    logger.info(f"Get experiment: {experiment_name}")
    
    return s3, experiment


# --------------------------------------------------------------------------------------------------------------------------------------------------
# Save preprocessor as an artifact with the relay of a tmp dir
# Saving preprocessor as an artifact
# joblib.dump needs write permission in the current dir 
# which may cause "[Errno 13] Permission denied: 'preprocessor.pkl'"
# while running fastapi/train_lr in container on HF Spaces
# So instead, dump in /tmp and from there save in S3
def _save_preprocessor_to_mlflow(preprocessor, artifact_subdir="preprocessing", filename="preprocessor.pkl"):
    """
    Save preprocessor as an MLflow artifact using a temporary directory.
    
    This avoids permission issues when running in containers (e.g., HF Spaces)
    by dumping to /tmp first, then uploading to MLflow/S3.
    
    Parameters:
    -----------
    preprocessor : sklearn preprocessor
        The fitted preprocessor to save
    artifact_subdir : str
        Subdir in artifacts section in experiments/runs/artifacts
    filename : str
        Name of the pickle file (default: "preprocessor.pkl")
    """
    logger.debug(f"Enter _save_preprocessor_to_mlflow")
    with tempfile.TemporaryDirectory() as tmp_dir:  # Create /tmp/tmpXXXX/
        preprocessor_path = os.path.join(tmp_dir, filename)
        logger.info(f"Create temporary file for joblib.dump: {preprocessor_path}")
        
        joblib.dump(preprocessor, preprocessor_path)
        
        mlflow.log_artifact(
            preprocessor_path,
            artifact_path=artifact_subdir
        )
        logger.info(f"Save preprocessor in Artifacts/{artifact_subdir}: {filename}")


# --------------------------------------------------------------------------------------------------------------------------------------------------
# Create a function to evaluate the fit result
def _evaluate_model_fit(train_score: float, test_score: float, threshold: float = 0.1) -> str:
    """
    Evaluate if model is overfitting, underfitting or well-fitted.
    Parameters:
    -----------
    train_score : float
        R² score on training set
    test_score : float
        R² score on test set
    threshold : float
        Maximum acceptable difference between train and test scores (default: 0.1)
    Returns:
    --------
    str : "good_fit", "overfitting", "underfitting", or "poor_fit"
    """
    score_diff = train_score - test_score
    
    # Case 1: Very low scores on both sides
    if train_score < 0.6 and test_score < 0.6:
        return "underfitting"
    
    # Case 2: High train score but significantly lower test score
    if score_diff > threshold and train_score > 0.7:
        return "overfitting"
    
    # Case 3: Both scores are close and acceptable
    if abs(score_diff) <= threshold and test_score >= 0.6:
        return "good_fit"
    
    # Case 4: Other problematic situations
    return "poor_fit"

# --------------------------------------------------------------------------------------------------------------------------------------------------
def train_lr(model_name: str="LinearRegression"):
    """
    Train a Linear Regression and use mlflow to track the experiment.   
    -------
    Parameters:
        model_name (str): name of the model to be stored in artifacts
    Returns:
    -------
    dict:
        metrics and coeff of the linear regression
    """
    
    logger.debug(f"Enter train_lr")
    # Apply the preprocessing to the dataset
    dataset, target, features, preprocessor, X_train, X_test, Y_train, Y_test = _apply_preprocessing()
    
    s3, experiment = _setup_boto_and_mlflow_experiment()
    
    with mlflow.start_run(experiment_id=experiment.experiment_id):
        logger.info(f"Start new run: {experiment.experiment_id}")
        
        # Train model
        model = LinearRegression()
        model.fit(X_train, Y_train)
        logger.debug(f"Fit model")
        
        # Saving model into the registry
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=model_name
        )
        logger.debug(f"Save model in registry: {model_name}")
        
        # Alias for the latest version in the registry
        alias_version = "Current"   # Our naming choice
        client = MlflowClient()
        # Retrieve the latest version of the registered model
        versions = client.get_latest_versions(model_name)
        latest_version = versions[0].version  # 0 is fine because get_latest_versions returns sorted list
        client.set_registered_model_alias(
            name=model_name,
            alias=alias_version,        # latest (case insensitive) is a reserved keyword
            version=latest_version
        )
        logger.debug(f"Set alias for the model in registry: {alias_version}")
                
        # Saving preprocessor as an artifact
        _save_preprocessor_to_mlflow(preprocessor)
        
        # Optionally return performance metrics
        Y_train_pred = model.predict(X_train)
        Y_test_pred = model.predict(X_test)
        train_score = r2_score(Y_train, Y_train_pred)
        test_score = r2_score(Y_test, Y_test_pred)
        logger.info(f"Train Score: {train_score}, Test Score: {test_score}")

        # Get coeff and rename some of them
        l_columns = []
        for name, pipeline, features_list in preprocessor.transformers_: # for each tuple
            if name == 'num': 
                l_features = features_list 
            else: 
                l_features = pipeline.named_steps['encoder'].get_feature_names_out()
                l_features = list(l_features)
                l_features = np.char.replace(l_features, 'x0', features_list[0])
                l_features = np.char.replace(l_features, 'x1', features_list[1])
            l_columns.extend(l_features) 
        # Transfom coeff in a dataframe        
        df_coefs = pd.DataFrame(
            index=l_columns,
            data=model.coef_.transpose(),
            columns=["coefficients"]
        )
        # Sort coeff by their relative importance and transform them in a dictionary
        d_features_importance = (
            df_coefs.sort_values(by='coefficients', key=abs)["coefficients"]
            .to_dict()
        )
        # Format the key/values in pure Python to avoid numpy.str_, pandas.Index...
        d_features_importance = {str(k): float(v) for k, v in d_features_importance.items()}
        
        return {
            "status": "success",
            "model_name": model_name,
            "model_evaluation": _evaluate_model_fit(train_score, test_score),
            "train_score": round(train_score, 3),
            "test_score": round(test_score, 3),
            "features_importance": d_features_importance    # dict type
        }

