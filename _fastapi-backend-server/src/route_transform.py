from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Logging
import logging

# Create route for transform entrypoints
transform_router = APIRouter()

from pipeline.core.src.transform import transform_pipeline
@transform_router.get("/transform_pipeline", include_in_schema=False)
def entrypoint_transform():
    """ Simulate transformation pipeline (route_transform)"""
    logging.getLogger("pipeline.core.src.transform").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        dataset = transform_pipeline()
        return {
            "status": "success",
            "rows": len(dataset),
            "columns": list(dataset.columns)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))