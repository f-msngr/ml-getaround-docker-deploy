from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Logging
import logging

# Create route for load entrypoints
load_router = APIRouter()


# ************************************************************************************************************
# Get the rentals dataset structure
# ************************************************************************************************************
from pipeline.core.src.load import get_rentals_stats
@load_router.get("/rentals_stats", summary="Get the dataset rentals structure in json")
def entrypoint_load_rentals_stats():
    """ Display json structure (shared route_load)"""
    logging.getLogger("pipeline.core.src.load").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        d_rentals = get_rentals_stats()
        return d_rentals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ************************************************************************************************************
# Get the whole rentals dataset as a dataframe - INVISBLE in swagger
# ************************************************************************************************************
from pipeline.core.src.load import get_rentals_as_json
@load_router.get("/rentals", include_in_schema=False)
def entrypoint_load_rentals():
    """ Load complete dataset (shared route_load)"""
    logging.getLogger("pipeline.core.src.load").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        return get_rentals_as_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ************************************************************************************************************
# Get one rental by its rental_id
# ************************************************************************************************************
from pydantic import BaseModel
from typing import Optional # Optional allows NaN value
# Define data model
class Rental(BaseModel):
    # Depending on the EDA (missing values %) on rentals dataset, NaN has to be managed as a return value
    rental_id: int
    car_id: int
    checkin_type: str
    state: str
    delay_at_checkout: Optional[int] = None
    previous_ended_rental_id: Optional[int] = None
    delta_with_previous: Optional[int] = None

from pipeline.core.src.load import get_rental_by_id
@load_router.get("/rentals/{rental_id}", summary="Get one specific rental")
def entrypoint_load_rental_by_id(rental_id: int)-> Rental:
    """ Retrieve one rental by its rental_id (shared route_load)"""
    logging.getLogger("pipeline.core.src.load").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    
    try:
        return get_rental_by_id(rental_id)
    except ValueError as e: # ValueError defined in get_rental_by_id in case rental_id doesn't exist in dataset    
        # 404 if rental-id not found
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # 500 if other problem
        raise HTTPException(status_code=500, detail=str(e))


# ************************************************************************************************************
# Get the cars dataset structure
# ************************************************************************************************************
from pipeline.core.src.load import get_cars_stats
@load_router.get("/cars_stats", summary="Get the dataset cars structure in json")
def entrypoint_load_cars_stats():
    """ Display json structure (shared route_load)"""
    logging.getLogger("pipeline.core.src.load").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        return get_cars_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ************************************************************************************************************
# Get the whole cars dataset as a dataframe - INVISBLE in swagger
# ************************************************************************************************************
from pipeline.core.src.load import get_cars_as_json
@load_router.get("/cars", include_in_schema=False)
def entrypoint_load_cars():
    """ Load complete dataset (shared route_load)"""
    logging.getLogger("pipeline.core.src.load").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        return get_cars_as_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
