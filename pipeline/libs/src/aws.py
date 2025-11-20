import os
import io

import pandas as pd
import joblib
import boto3
from botocore.exceptions import ClientError

# Give access to env variables
from dotenv import load_dotenv
load_dotenv()   # factorize env variables loading for all functions

# Internal
from pipeline.libs.src.utils import get_project_name

# Logging
import logging
logger = logging.getLogger(__name__)


def serialize_to_s3(object_name: object, s3_key: str) -> bool:
    """
    Serializes an object in memory to S3 bucket
    The function authenticates using AWS credentials stored in environment variables:
    - AWS_ACCESS_KEY
    - AWS_SECRET_KEY
    - AWS_REGION
    - AWS_S3_BUCKET
    
    Parameters:
    -----------
    object_name : object
        Object to serialize
    s3_key : str
        The key (path) of the file in the S3 bucket.
    
    Raises:
    ------
    ClientError :
        If there is an error related to AWS credentials or access.
    Exception :
        For any unexpected issues.
    """
    try:
        # Creating buffer in memory
        buffer = io.BytesIO()
        joblib.dump(object_name, buffer)
        buffer.seek(0)  # Needs to be set before read/upload
        
        # Configure bucket
        aws_s3_bucket = os.getenv('AWS_S3_BUCKET')
        logger.info(f"Serializing object to S3: s3://{aws_s3_bucket}/{s3_key}")
        
        # Create an S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
            )
        
        # Serialize the object to S3
        s3_client.upload_fileobj(
            Fileobj=buffer,
            Bucket=aws_s3_bucket,
            Key=s3_key
            )
        object_type = type(object_name)
        logger.info(f"Type of Object ready for serializing to S3: {object_type}")
        logger.info(f"Object successfully serialized to S3: s3://{aws_s3_bucket}/{s3_key}")
        
        # Verify that the file exists in S3
        s3_client.head_object(
            Bucket=aws_s3_bucket,
            Key=s3_key
            )
        logger.info(f"Verification successful - The file exists in S3")
        
        return True
        
    except ClientError as e:
        logger.error(f"Error during serialization to S3: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise



def get_serialized_from_S3(s3_key: str) -> object:
    """
    Loads a a file in memory from a private S3 bucket.

    The function authenticates using AWS credentials stored in environment variables:
    - AWS_ACCESS_KEY
    - AWS_SECRET_KEY
    - AWS_REGION
    - AWS_S3_BUCKET

    Parameters:
    ----------
    s3_key : str
        The key (path) of the file in the S3 bucket.

    Returns:
    -------
    obj:
        An object if the file is successfully loaded,
        or False if an error occurs during the process.

    Raises:
    ------
    ClientError :
        If there is an error related to AWS credentials or access.
    Exception :
        For any unexpected issues.
    """
    try:
        # Configure bucket
        aws_s3_bucket = os.getenv('AWS_S3_BUCKET')
        logger.info(f"Deserializing the file from S3: s3://{aws_s3_bucket}/{s3_key}")
        
        # Create an S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
            )
        
        # Get serialized object from file in S3
        response = s3_client.get_object(
            Bucket=aws_s3_bucket,
            Key=s3_key
            )
        logger.info(f"File successfully loaded from S3: s3://{aws_s3_bucket}/{s3_key}")
        serialized_obj = joblib.load(io.BytesIO(response['Body'].read()))
        object_type = type(serialized_obj)
        logger.info(f"Type of Object deserialized from S3: {object_type}")
        
        logger.info(f"Object successfully deserialized from S3.")
        
        return serialized_obj
        
    except ClientError as e:
        logger.error(f"Error during deserialization from S3: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


def get_from_bucket(path_to_object: str) -> object:
    """
    Get object from the internal path inside a bucket in S3 (assume existing objet)
    Parameter:
    -----------
    path_to_object : str
        relative path of object in bucket root in S3
    
    Returns:
    -------
    obj:
        An object if the file is successfully loaded,
        or False if an error occurs during the process.
    """
    logger.info(f"Path to object to extract relatively to project root: {path_to_object}")
    
    # project_root_path defined by PROJECT_NAME in .env
    project_root_path = get_project_name()

    # Deserialize from Bucket/Project/...
    s3_key = f'{project_root_path}/{path_to_object}'
    logger.info(f"S3 key relative to bucket root: {s3_key}")

    # Get from S3: S3_key = file path relative to bucket name defined in ENV
    df = get_serialized_from_S3(s3_key)
    
    return df


def save_to_bucket(object_name: object, path_to_object: str) -> bool:
    """
    Save an object in a bucket to a specific path.
    Parameters:
    -----------
    object_name : object
        Object to save
    path_to_object : str
        The path of the file in the S3 bucket.
    Returns:
    -------
    bool:
        True if the file is saved with no error
    """
    logger.info(f"Path to save the {object_name} relatively to project root: {path_to_object}")
    
    # project_root_path defined by PROJECT_NAME in .env
    project_root_path = get_project_name()

    # Serialize to Bucket/Project/...
    s3_key = f'{project_root_path}/{path_to_object}'
    logger.info(f"S3 key relative to bucket root: {s3_key}")

    s3_key = f'{project_root_path}/{path_to_object}'
    
    return serialize_to_s3(object_name, s3_key)