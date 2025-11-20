# Imports
import sys
import os
import io
sys.path.append('..')

# Logging
import logging
logger = logging.getLogger(__name__)

# Internal
from pipeline.libs.src.utils import get_project_name
from pipeline.libs.src.aws import get_serialized_from_S3, serialize_to_s3, get_from_bucket, save_to_bucket


def extract_pipeline():

    # *******************************************************************************************
    # THIS PART IS MEANT TO BE REPLACED BY A REAL EXTRACT PROCESS PIPELINE
    # AND NOT A DUMMY ONE CONSISTING OF DESERIALIZATION/CSV READ
    # Read dataset from S3 (assume existing objet)
    # Extract csv and serialize as pandas dataframe in .pkl
    path_to_initial_raw_data = f'data/raw/data_to_extract.csv'
    dataset = get_from_bucket(path_to_initial_raw_data)
    
    path_to_extracted_data = f'data/raw/extracted_data_converd_in_pkl.pkl'
    save_to_bucket(dataset, path_to_extracted_data)   
    # *******************************************************************************************

    return dataset