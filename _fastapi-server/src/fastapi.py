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
    root_path="/api",
    title="🚗 GetAround - 🌐 Frontend API",
    description="Frontend API for GetAround Business Case",
    version="1.0.0"
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI: 🌐 Frontend server -> Up and Running ✅"}

# ************************************************************************************************************
# Use routes to separate functionnal parts
#from fastapi import APIRouter
#router = APIRouter()

# ************************************************************************************************************
# shared files mounted by bind mounts with docker-compose
# have to be copied in each frontend and backend container
# because /_fastapi-servers-shared/src/shared cannot be shared whithout bind mount

# Include router
from .shared.route_load import load_router
app.include_router(load_router)

from .shared.route_predict import predict_router
app.include_router(predict_router)