
# Imports
import sys
import os
import io
sys.path.append('..')

# Logging
import logging
logger = logging.getLogger(__name__)

import pandas as pd

# Internal
from pipeline.libs.src.utils import get_project_name
from pipeline.libs.src.aws import get_serialized_from_S3, serialize_to_s3, get_from_bucket, save_to_bucket


def dummy_mod_col(df):
    # Dummy transformation: nothing

    logger.info(f"Transform by doing nothing: {df.columns}")
    
    
    logger.info(f"Transformed columns: {df.columns}")
    return df


def dummy_add_col_area(df):
    # Add 0 new column

    logger.info(f"Create 0 column: {df.columns}")
    
    logger.info(f"Created 0 column: {df.columns}")
    return df



def transform_pipeline():

    # *******************************************************************************************
    # THIS PART IS MEANT TO BE REPLACED BY A REAL TRANSFORM PROCESS PIPELINE
    # AND NOT A DUMMY ONE CONSISTING OF USELESS TRANSFORMATION
    # Read dataset from S3 (assume existing objet)
    # Read dataset as pandas dataframe in .pkl, apply transform pipeline, and serialize as pandas dataframe in .pkl
    path_to_initial_data = f'data/raw/PICKEL_TO_PICKELIZE.pkl'
    dataset = get_from_bucket(path_to_initial_data)
    
    # TRANSFORM
    logger.info(f"Apply transform pipeline to data")
    # Add columnn
    # dataset = dummy_add_col_area(dataset)
    # Modify columns values
    dataset = dummy_mod_col(dataset)
    
    path_to_transformed_data = f'data/transformed/PICKEL_TO_PICKELIZE_transformed.pkl'
    save_to_bucket(dataset, path_to_transformed_data)
    # *******************************************************************************************
      
    return dataset