# Dockerfile for DEPLOYMENT OF FastAPI+Streamlit+nginx
# _CONF/deploy/frontend_deploy_dir/Dockerfile.txt
# Dockerfile used for frontend server image
# Step 1: lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    lsof \
    net-tools \
    procps \
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

# Set working directory
WORKDIR /app

# Set environment variables
ENV PROJECT_NAME="deplmt-templ-ng-st-fa-mf"
ENV PROJECT_ROOT="/app"
ENV PYTHONPATH="/app/api:/app"
ENV URL_API="http://localhost:$PORT_REV_PROXY_FRONTEND_EXTERNAL/api"

# Copy nginx configuration files
# First remove default conf
# Then replace with personal default.conf
RUN rm -f /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/conf.d
COPY ./nginx/default.conf /etc/nginx/nginx.conf
# Configure nginx home page + local directory
COPY ./nginx/html/ /etc/nginx/html/

# Copy application files
COPY ./streamlit ./streamlit
COPY ./api ./api

# Redirect Streamlit to an accessible directory
ENV STREAMLIT_CONFIG_PATH="/tmp/.streamlit"
RUN mkdir -p /tmp/.streamlit
RUN chmod 755 /tmp/.streamlit






# COPY pipeline/ to provide utils in the image
COPY ./pipeline ./pipeline

# Copy configuration files
COPY ./requirements.txt .
COPY ./start.sh .
# Make the script executable
RUN chmod ug+x ./start.sh

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by nginx
EXPOSE $PORT_REV_PROXY_FRONTEND_EXPOSED

# Allow /app/pipeline to be imported as a Python module
# pipeline mounted as volume in docker-compose.yml
ENV PYTHONPATH="/app/pipeline:${PYTHONPATH}"

# Start services
CMD ["./start.sh"]
