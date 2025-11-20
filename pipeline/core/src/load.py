# Imports
import sys
import os
import io
sys.path.append('..')

# Logging
import logging
logger = logging.getLogger(__name__)

import pandas as pd
from typing import Any

# Internal
from pipeline.libs.src.utils import get_project_name
from pipeline.libs.src.aws import get_serialized_from_S3, get_from_bucket


# ************************************************************************************************************
# RENTALS
# ************************************************************************************************************
def get_rentals() -> pd.DataFrame:
    """
    Return a dataframe from dataset of rentals in .pkl format from a bucket.
    """
    path_to_rentals_data = f'data/raw/df_rentals.pkl'
    dataset = get_from_bucket(path_to_rentals_data)
    return dataset


def get_rentals_as_json() -> list[dict[str, Any]]:
    """
    Return a json as a list of dict.
    """
    try:
        df_rentals = get_rentals()
        # convert dataframe to json
        return df_rentals.to_dict(orient="records")
    except Exception as e:
        raise RuntimeError(f"Failed to convert DataFrame to JSON: {e}")


def get_rentals_stats() -> dict:
    """
    Return rentals json main statistics as a dictionary
    """
    try:
        d_stats = {}
        df_rentals = get_rentals()
        d_stats["length"] = df_rentals.shape[0]
        d_stats["width"] = df_rentals.shape[1]
        d_stats["columns"] = df_rentals.columns.to_list()
        return d_stats
    
    except Exception as e:
        raise RuntimeError(f"Failed to convert DataFrame to JSON: {e}")



def get_rental_by_id(rental_id: int)-> dict:
    """
    Return a single rental by its ID, or raise a clear error if not found..
    """
    df_rentals = get_rentals()
    
    # Filter
    rental = df_rentals.loc[df_rentals['rental_id'] == rental_id]
    logger.info(f"Extracting rental_id {rental_id} - type(rental): {type(rental)} — shape: {rental.shape}")
    
    if rental.empty:
        msg = f"🐇: rental_id {rental_id} not found in dataset"
        logger.warning(msg)
        raise ValueError(msg)
    
    try:
        return rental.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Unexpected error converting rental_id {rental_id} to dict: {e}")
        raise RuntimeError(f"Failed to retrieve rental_id {rental_id} from rentals dataset") from e


# ************************************************************************************************************
# CARS
# ************************************************************************************************************
def get_cars() -> pd.DataFrame:
    """
    Return a dataframe from dataset of cars in .pkl format from a bucket.
    """
    path_to_rentals_data = f'data/transformed/df_cars_transformed.pkl'
    dataset = get_from_bucket(path_to_rentals_data)
    return dataset


def get_cars_as_json() -> list[dict[str, Any]]:
    """
    Return a json as a list of dict.
    """
    try:
        df_cars = get_cars()
        # convert dataframe to json
        return df_cars.to_dict(orient="records")
    except Exception as e:
        raise RuntimeError(f"Failed to convert DataFrame to JSON: {e}")


def get_cars_stats() -> dict:
    """
    Return cars json main statistics as a dictionary
    """
    try:
        d_stats = {}
        df_cars = get_cars()
        d_stats["length"] = df_cars.shape[0]
        d_stats["width"] = df_cars.shape[1]
        d_stats["columns"] = df_cars.columns.to_list()
        return d_stats
    
    except Exception as e:
        raise RuntimeError(f"Failed to convert DataFrame to JSON: {e}")
