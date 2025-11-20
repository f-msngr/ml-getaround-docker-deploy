#!/bin/bash
set -e

export PYTHONPATH=/app:/app/api-backend

# Lancer FastAPI
uvicorn src.fastapi:app --host 0.0.0.0 --port $PORT_FASTAPI_BACKEND_EXPOSED  --reload &


# Démarrer Nginx en dernier plan (bloquant)
exec nginx -g 'daemon off;'