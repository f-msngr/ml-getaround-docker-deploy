# Build from a LINUX lightweight version of Anaconda
FROM continuumio/miniconda3

# Update packages and install nano unzip and curl
RUN apt-get update
RUN apt-get install nano unzip curl -y

# Install AWS cli - Necessary since we are going to interact with S3 
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# FOR DEPLOYMENT ON HF SPACES, SET THESE ENV AS SECRETS

ARG PORT_MLFLOW_TRACKING_EXTERNAL
#ARG AWS_ACCESS_KEY
#ARG AWS_SECRET_KEY
#ARG BACKEND_STORE_URI
#ARG ARTIFACT_ROOT

ENV PORT_MLFLOW_TRACKING_EXTERNAL=${PORT_MLFLOW_TRACKING_EXTERNAL}
#ENV AWS_ACCESS_KEY=${AWS_ACCESS_KEY}
#ENV AWS_SECRET_KEY=${AWS_SECRET_KEY}
#ENV BACKEND_STORE_URI=${BACKEND_STORE_URI}
#ENV ARTIFACT_ROOT=${ARTIFACT_ROOT}


# THIS IS SPECIFIC TO HUGGINGFACE
# We create a new user named "user" with ID of 1000
RUN useradd -m -u 1000 user
# We switch from "root" (default user when creating an image) to "user" 
USER user
# We set two environment variables 
# so that we can give ownership to all files in there afterwards
# we also add /home/user/.local/bin in the $PATH environment variable 
# PATH environment variable sets paths to look for installed binaries
# We update it so that Linux knows where to look for binaries if we were to install them with "user".
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# We set working directory to $HOME/app (<=> /home/user/app)
WORKDIR $HOME/app

# Copy all local files to /home/user/app with "user" as owner of these files
# Always use --chown=user when using HUGGINGFACE to avoid permission errors
COPY --chown=user . $HOME/app

# Copy and install dependencies 
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# App listening port inside container
EXPOSE $PORT_MLFLOW_TRACKING_EXTERNAL

# Copy of run script
COPY run.sh /run.sh
USER root
RUN chmod +x /run.sh
USER user

# Launch mlflow server 
CMD ["/run.sh"]