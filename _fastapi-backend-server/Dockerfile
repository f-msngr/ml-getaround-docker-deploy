# Dockerfile used for back end server image
# Lightweight base image
FROM python:3.11-slim

ARG PORT_FASTAPI_BACKEND_EXPOSED
ENV PORT_FASTAPI_BACKEND_EXPOSED=${PORT_FASTAPI_BACKEND_EXPOSED}

# To avoid: Failed to import Git (the Git executable is not on the PATH)
# ->install  git
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*
# Install system dependencies for debugging from within the container
# RUN apt-get update && apt-get install -y \
#    curl \
#    lsof \
#    net-tools \
#    procps \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# Sets the working directory for the API
WORKDIR /app

# Set environment variables
ENV PROJECT_NAME="deplmt-templ-ng-st-fa-mf"
ENV PROJECT_ROOT="/app"
ENV PYTHONPATH="/app/api-backend:/app"

# Copy necessary files into the image
# In local development, this will be overwritten by a volume mount
# Create the working directory explicitly
# so it can be used in the WORKDIR directive
# because the api-backend volume is bind-mounted by docker-compose
RUN mkdir -p /app/api-backend
COPY ./_fastapi-backend-server/__init__.py ./api-backend

# Copy configuration files
COPY ./_fastapi-backend-server/requirements.txt .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the backend API port
EXPOSE $PORT_FASTAPI_BACKEND_EXPOSED

# Allow /app/pipeline to be imported as python module
# pipeline mounted as volume in docker-compose.yml
ENV PYTHONPATH="/app/pipeline:${PYTHONPATH}"

# Set api-backend as working directory
WORKDIR /app/api-backend
# Command to launch FastAPI via Uvicorn
CMD ["sh", "-c", "uvicorn src.fastapi:app --host 0.0.0.0 --port=$PORT_FASTAPI_BACKEND_EXPOSED --reload"]