from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Logging
import logging

# Create route for predict entrypoints
predict_router = APIRouter()

# --------------------------------------------------------------------------------------------------------------------------------------------------
from pydantic import BaseModel, Field
# Input model
# Define format of input data
class CarInputData(BaseModel):
    """Input data model for car rental price prediction."""
    
    model_key: str = Field(..., description="Car model/brand (e.g., 'BMW', 'Renault')")
    mileage: int = Field(..., ge=0, description="Mileage in km")
    engine_power: int = Field(..., gt=0, description="Engine power in horsepower")
    fuel: str = Field(..., description="Fuel type (e.g., 'petrol', 'diesel', 'electric')")
    paint_color: str = Field(..., description="Paint color (e.g., 'black', 'white', 'red')")
    car_type: str = Field(..., description="Car type (e.g., 'sedan', 'suv', 'hatchback')")
    private_parking_available: bool = Field(..., description="Private parking available")
    has_gps: bool = Field(..., description="GPS available")
    has_air_conditioning: bool = Field(..., description="Air conditioning available")
    automatic_car: bool = Field(..., description="Automatic transmission")
    has_getaround_connect: bool = Field(..., description="Getaround Connect feature")
    has_speed_regulator: bool = Field(..., description="Speed regulator/cruise control")
    winter_tires: bool = Field(..., description="Winter tires equipped")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_key": "BMW",
                "mileage": 50000,
                "engine_power": 150,
                "fuel": "petrol",
                "paint_color": "black",
                "car_type": "sedan",
                "private_parking_available": True,
                "has_gps": True,
                "has_air_conditioning": True,
                "automatic_car": False,
                "has_getaround_connect": True,
                "has_speed_regulator": True,
                "winter_tires": False
            }
        }

# Output prediction model
# Define format of output data
class CarPricePrediction(BaseModel):
    predicted_price: float = Field(..., description="Predicted rental price per day in €")

import pandas as pd
from pipeline.core.src.predict import predict_car_price_with_lr_model
@predict_router.post(
    "/predict_lr", 
    summary="Predict car rental price 💰 with Linear Regression",
    response_model=CarPricePrediction
)
def entrypoint_predict_lr(data: CarInputData) -> CarPricePrediction:
    """Predict rental price per day using Linear Regression model."""
    logging.getLogger("pipeline.core.src.predict").setLevel(logging.DEBUG)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)

    try:
        # Convert input to DataFrame
        df_features = pd.DataFrame([data.model_dump()])
        
        # Predict
        prediction = predict_car_price_with_lr_model(df_features)
        
        # Return rounded prediction
        return CarPricePrediction(predicted_price=round(prediction, 2))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")