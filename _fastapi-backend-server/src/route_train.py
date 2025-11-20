from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Logging
import logging

# Create route for train entrypoints
train_router = APIRouter()


# ************************************************************************************************************
# Train Linear Regression
# ************************************************************************************************************
from pydantic import BaseModel
from typing import Dict
# Define data model
class LR_Response(BaseModel):
    status: str
    model_name: str
    model_evaluation: str
    train_score: float
    test_score: float
    features_importance: Dict[str, float]


from pipeline.core.src.train import train_lr
@train_router.get("/train_lr", summary="Train linear regression", response_model=LR_Response)
def entrypoint_train_lr() -> LR_Response:
    """ Train model (route_train)"""
    logging.getLogger("pipeline.core.src.train").setLevel(logging.WARNING)   # SET to WARNING to disable logging in server console
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        return train_lr()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))