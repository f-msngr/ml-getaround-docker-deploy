#!/bin/bash
set -e

export PYTHONPATH=/app

# Lancer FastAPI
uvicorn api.src.fastapi:app --host 0.0.0.0 --port $PORT_FASTAPI_EXTERNAL &

# Lancer Streamlit
streamlit run streamlit/src/streamlit.py --server.port=$PORT_STREAMLIT_EXTERNAL --server.address=0.0.0.0 --server.baseUrlPath=/dashboard &

# Démarrer Nginx en dernier plan (bloquant)
nginx -g 'daemon off;'