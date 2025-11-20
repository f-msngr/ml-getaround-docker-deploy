from fastapi import Request, HTTPException, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Logging
import logging

# Create route for extract entrypoints
extract_router = APIRouter()

from pipeline.core.src.extract import extract_pipeline
@extract_router.get("/extract_pipeline", include_in_schema=False)
def entrypoint_extract():
    " Dummy extraction process (route_extract)"
    logging.getLogger("pipeline.core.src.extract").setLevel(logging.WARNING)
    logging.getLogger("pipeline.libs.src.aws").setLevel(logging.WARNING)
    try:
        dataset = extract_pipeline()
        return {
            "status": "success",
            "rows": len(dataset),
            "columns": list(dataset.columns)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
