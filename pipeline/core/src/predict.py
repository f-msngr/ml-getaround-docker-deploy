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
import joblib

# Internal
from pipeline.libs.src.utils import get_project_name
from pipeline.libs.src.aws import get_serialized_from_S3



# --------------------------------------------------------------------------------------------------------------------------------------------------
# Setup the AWS connection with boto, using AWS creds in .env
# And Setup MLflow client
from typing import Any
from mlflow.tracking import MlflowClient
def _setup_boto_and_mlflow_client()-> tuple[Any, MlflowClient]:
    """ 
    This function sets some env variables with some other .env variables
    Returns:
    -------
    tuple[Any, MlflowClient]:
        - S3Client: Configured boto3 S3 client
        - MlflowClient: MLflow tracking client
    """
    logger.debug(f"Enter setup_boto_and_mlflow")
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
    logger.debug(f"Set MLFLOW_TRACKING_URI with TRACKING_URI: {os.getenv('TRACKING_URI')}")

    # Set Mlflow client
    client = MlflowClient()

    return s3, client


# --------------------------------------------------------------------------------------------------------------------------------------------------
# Predict from loaded model
def predict_car_price_with_lr_model(
    df_features: pd.DataFrame,
    model_name: str="LinearRegression",
    alias_version: str="Current",
    ) -> np.ndarray:
    """
    Predict the target Y (i.e. rental_price_per_day) from input features using the lr trained model.

    Parameters:
    - df_features (pd.DataFrame): DataFrame containing features columns.

    Returns:
    - np.ndarray: numpy array of predicted target
    """
    logger.info(f"Predict price with linear model")
    logger.debug(f"Enter predict_car_price_with_lr_model")
    # Client
    # Set and Get MLflow Client
    _, client = _setup_boto_and_mlflow_client()
    # Model
    # Retrieve the latest version of the registered model - alias "Current" cf. train.py
    latest_version = client.get_model_version_by_alias(model_name, alias_version)
    logger.debug(f"Get the aliased '{alias_version}' version of the model: {model_name}")
    # Run
    # Get the run that is associated to the model
    run_id = latest_version.run_id
    logger.debug(f"Get run_id associated to aliased '{alias_version}' version: {run_id}")

    # Preprocessor
    # Get the preprocessor to preprocess the input user data
    # See preprocessor artifact storage in train.py
    preprocessor_uri = f"runs:/{run_id}/preprocessing/preprocessor.pkl"
    preprocessor_path = mlflow.artifacts.download_artifacts(preprocessor_uri)
    preprocessor = joblib.load(preprocessor_path)
    logger.debug(f"Loaded preprocessor from {preprocessor_uri}")
    # Apply preprocessing to raw features
    X_preprocessed = preprocessor.transform(df_features)
    logger.debug(f"Preprocessed features shape: {X_preprocessed.shape}")
    
    # Load model
    # Load the last one - get it by the alias (cf. train.py)
    model = mlflow.sklearn.load_model(f"models:/{model_name}@{alias_version}")
    
    target_pred = model.predict(X_preprocessed) # np.ndarray shape (1,)
    logger.debug(f"Target Prediction on Features: {df_features}: {target_pred}")
    
    # Return Prediction
    # Safety clamp : return 0 if target<0      
    pred = float(target_pred[0])   # convert to python float
    pred = max(pred, 0.0)          # clamp non négatif
    return pred


