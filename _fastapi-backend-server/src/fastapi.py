import os
import io
import sys

from fastapi import FastAPI, Request, HTTPException, Form, Response, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel

import joblib
from pathlib import Path

import numpy as np
import pandas as pd


# ************************************************************************************************************
# Logging
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# ************************************************************************************************************
# Environment
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Give access to env variables
project_root_path = os.getenv("PROJECT_ROOT")
project_dir_name = os.getenv("PROJECT_NAME")

# ************************************************************************************************************
# Set root_path for nginx
app = FastAPI(
    root_path="/api-backend",
    title="🚗 GetAround - ⚙️ Backend API",
    description="Backend API for GetAround Business Case",
    version="1.0.0"
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI: ⚙️ Backend server -> Up and Running ✅"}

# ************************************************************************************************************
# Use routes to separate functionnal part
from fastapi import APIRouter
router = APIRouter()

# ************************************************************************************************************
# Include router
from .route_auth import auth_router
app.include_router(auth_router)

from .route_extract import extract_router
app.include_router(extract_router)

from .route_transform import transform_router
app.include_router(transform_router)

from .route_train import train_router
app.include_router(train_router)
# ************************************************************************************************************
# Shared routes in _fastapi-servers-shared/src/
# For local dev:
# shared routes mounted by bind mounts with docker compose cf. docker-compose.yml
# For predeployment:
# need to dupplicate shared routes:
# shared routes copied from _fastapi-servers-shared/src/
# in each frontend and backend container

# Include router
from .shared.route_load import load_router
app.include_router(load_router)

from .shared.route_predict import predict_router
app.include_router(predict_router)

# ************************************************************************************************************


# ************************************************************************************************************
