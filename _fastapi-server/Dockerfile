# Lightweight base image
FROM python:3.11-slim

ARG PORT_FASTAPI_EXPOSED
ENV PORT_FASTAPI_EXPOSED=${PORT_FASTAPI_EXPOSED}

ENV PYTHONPATH="/app/api:/app"

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#    curl \
#    lsof \
#    net-tools \
#    procps \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# Set the working directory specific to the API
WORKDIR /app

# Copy necessary files into the image
# In local development, this will be overwritten by a volume mount
# Explicitly create the working directory
# so it can be referenced in the WORKDIR directive
# because the 'api' volume is bind-mounted via docker-compose
RUN mkdir -p /app/api
COPY ./_fastapi-server/__init__.py ./api

# Copy configuration files
COPY ./_fastapi-server/requirements.txt .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE $PORT_FASTAPI_EXPOSED

# Allow /app/pipeline to be imported as python module
# pipeline mounted as volume in docker-compose.yml
ENV PYTHONPATH="/app/pipeline:${PYTHONPATH}"

# Set 'api' as the working directory
WORKDIR /app/api
# Command to launch FastAPI via Uvicorn
CMD ["sh", "-c", "uvicorn src.fastapi:app --host 0.0.0.0 --port=$PORT_FASTAPI_EXPOSED --reload"]