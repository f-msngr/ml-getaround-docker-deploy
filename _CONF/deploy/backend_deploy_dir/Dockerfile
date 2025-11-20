# _CONF/deploy/backend_deploy_dir/Dockerfile.txt
# Dockerfile used for backend server image
# Lightweight base image
FROM python:3.11-slim

#ARG PORT_FASTAPI_BACKEND_EXPOSED
#ENV PORT_FASTAPI_BACKEND_EXPOSED=${PORT_FASTAPI_BACKEND_EXPOSED}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    lsof \
    net-tools \
    procps \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# THIS IS SPECIFIC TO HUGGINGFACE
# We create a new user named "user" with ID of 1000
#RUN useradd -m -u 1000 user
# We switch from "root" (default user when creating an image) to "user" 
#USER user
# We set two environment variables 
# so that we can give ownership to all files in there afterwards
# we also add /home/user/.local/bin in the $PATH environment variable 
# PATH environment variable sets paths to look for installed binaries
# We update it so that Linux knows where to look for binaries if we were to install them with "user".
#ENV HOME=/home/user
#ENV PATH=/home/user/.local/bin:$PATH

# Copy all local files to /home/user/app with "user" as owner of these files
# Always use --chown=user when using HUGGINGFACE to avoid permission errors
#COPY --chown=user . $HOME/app


# Create the working directory specific to the API
# MUST BE THE SAME AS IN docker-compose.yaml services/api/volumes
WORKDIR /app

# Set Environment variable
ENV PROJECT_NAME="deplmt-templ-ng-st-fa-mf"
ENV PROJECT_ROOT="/app"
ENV PYTHONPATH="/app/api-backend:/app"
ENV URL_API="http://localhost:$PORT_FASTAPI_BACKEND_EXPOSED/api-backend"

# Copy nginx configuration files
# First remove default conf
# Then replace with custom default.conf
RUN rm -f /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/conf.d
COPY ./nginx/default.conf /etc/nginx/nginx.conf
# Config nginx home page + dir from local
COPY ./nginx/html/ /etc/nginx/html/

# Copy the required files into the image
# Copy only necessary files
# With volume mounting, in local development, the entire directory will be mounted
COPY ./api-backend ./api-backend
COPY ./pipeline ./pipeline

# Copy configuration files
COPY ./requirements.txt .

COPY ./start.sh .
# Make the script executable
RUN chmod ug+x ./start.sh

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Set cache dir for mlflow tracking within API mlflow calls
ENV USER=user \
    HOME=/tmp \
    MLFLOW_TRACKING_USERNAME=user \
    MPLCONFIGDIR=/tmp/matplotlib \
    MATPLOTLIB_CACHE_DIR=/tmp/matplotlib
# Create dirs with write permissions
RUN mkdir -p /tmp/matplotlib /tmp/mlflow
RUN chmod 777 /tmp/matplotlib /tmp/mlflow



# Expose reverse proxy port to HF Spaces external port = 7860
EXPOSE $PORT_REV_PROXY_BACKEND_EXPOSED
# Expose API port
EXPOSE $PORT_FASTAPI_BACKEND_EXPOSED

# Allow /app/pipeline to be imported as python module
# pipeline mounted as volume in docker-compose.yml
ENV PYTHONPATH="/app/pipeline:${PYTHONPATH}"

# Start services
CMD ["./start.sh"]
