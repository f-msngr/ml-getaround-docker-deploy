# Deployment

[🔙 Back to README](../README.md#table-of-contents)

# Table of Contents

- [Deployment](#deployment)
- [Table of Contents](#table-of-contents)
- [Local Pre deployment 🏗️](#local-pre-deployment-️)
  - [Build](#build)
  - [Servers run (frontend + backend)](#servers-run-frontend--backend)
    - [Interactive mode - shell access](#interactive-mode---shell-access)
  - [MLFlow + deployment setup](#mlflow--deployment-setup)
    - [AWS Setup](#aws-setup)
    - [Database Setup (NeonDB)](#database-setup-neondb)
    - [Environment Variables](#environment-variables)
- [HuggingFace Spaces deployment 🤗](#huggingface-spaces-deployment-)
  - [MLFlow Server space](#mlflow-server-space)
  - [Frontend Server space](#frontend-server-space)
  - [Backend Server space](#backend-server-space)


# Local Pre deployment 🏗️

## Build

In production, local volumes are replaced by a distributed architecture, managed by a MLFlow server with access to a remote artifact store (AWS S3), and a remote PostgreSQL database for metrics.  
Access to these resources is configured through the .env file (not versioned), which ensures that sensitive values remain secure in production.
(.env.example should have already been modified and renamed to .env to match your own configuration)

``` bash
# Edit and modify MLFLOW_PROXY_PASS in .env  
# To match MLFlow server address on HF since nginx will redirect to this server url
nano .env
# Local predeployment build command will recreate the deploy dirs, modify some ports, build the images and be ready to run the containers
make build
```

This will remove all previous images, create 3 ready for deployment directories based on servers' configuration in _CONF/:  
- `frontend_deploy_dir/`: end user access (dashboard + basic API functionalities),
- `backend_deploy_dir/`: developer access (ETL advanced API functionalities + MLFlow access)
- `mlflow_deploy_dir/` : mlflow ready to deploy

[⬆ Back to top](#table-of-contents)

## Servers run (frontend + backend)

``` bash
# Local deployment servers start:
# make run: see make help  
# make run IMG=fe I=y (runs frontend image in interactive mode (ie shell access in container))
make run IMG=fe I=y
# In a new terminal:
make run IMG=be I=y
# Read more
make help
```

Open frontend interface in browser with port ```$PORT_REV_PROXY_FRONTEND_EXTERNAL``` defined in .env (default port: 7860):  
`http://localhost:7860/`  
<img src='../assets/screenshots/home_local_deploy_frontend.png' alt='local deploy_frontend home page' width='300'>  

Open backend interface in browser with port ```$PORT_REV_PROXY_BACKEND_EXTERNAL``` defined in .env (default port: 7861):  
`http://localhost:7861/`  
<img src='../assets/screenshots/home_local_deploy_backend.png' alt='local deploy_backend home page' width='300'>

[⬆ Back to top](#table-of-contents)

### Interactive mode - shell access

``` bash
# Access shell in containers in interactive mode with:
# frontend container:
make shell CONTAINER=fe
# backend container:
make shell CONTAINER=be
# Remove all containers, images, and automatically created directories:
make clean
```
[⬆ Back to top](#table-of-contents)

## MLFlow + deployment setup

### AWS Setup  
You should already have IAM + S3 from Local dev configuration steps.  
1. Create IAM user with S3 permissions
2. Generate access keys.  
3. Create S3 bucket: `s3://your-bucket-name/your-project/`

### Database Setup (NeonDB)
1. Create account at neon.tech (for example)
2. Create database
3. Get connection string

### Environment Variables
Update your `.env` file:
```bash
# Edit and modify .env
nano .env
AWS_REGION=your-region
AWS_ACCESS_KEY=your-key
AWS_SECRET_KEY=your-secret
ARTIFACT_ROOT=s3://your-bucket/artifacts
BACKEND_STORE_URI=postgresql://user:pass@host:port/db
```
[⬆ Back to top](#table-of-contents)


# HuggingFace Spaces deployment 🤗

Create New Blank Public Docker Space for each server on HF Space

## MLFlow Server space

Create ```<MLFLOW-SERVER-ML-DEPLMT-TEMPL>```

Set HF env as SECRETS
- AWS_REGION  
- AWS_ACCESS_KEY
- AWS_SECRET_KEY
- ARTIFACT_ROOT
- BACKEND_STORE_URI

```bash
# Set HF_MLFLOW_SERVER in .env to match <MLFLOW-SERVER-ML-DEPLMT-TEMPL> name
nano .env
HF_MLFLOW_SERVER=<MLFLOW-SERVER-ML-DEPLMT-TEMPL>
# Create HF deploy server config dir (with HF port map (default 7860))
# Clone <MLFLOW-SERVER-ML-DEPLMT-TEMPL>
# git add, commit, push
make push SERVER=mf MSG="Initial commit"
```
[⬆ Back to top](#table-of-contents)

## Frontend Server space

Create ```<FRONTEND-SERVER-ML-DEPLMT-TEMPL>```

Set SECRETS
- PROJECT_NAME
- AWS_REGION
- AWS_ACCESS_KEY
- AWS_SECRET_KEY
- AWS_S3_BUCKET
- TRACKING_URI

```bash
# Set HF_FE_SERVER in .env to match <FRONTEND-SERVER-ML-DEPLMT-TEMPL> name
nano .env
HF_FE_SERVER=<FRONTEND-SERVER-ML-DEPLMT-TEMPL>
# Create and push frontend server
make push SERVER=fe MSG="Initial commit"
```
[⬆ Back to top](#table-of-contents)

## Backend Server space

Create ```<BACKEND-SERVER-ML-DEPLMT-TEMPL>```

Set SECRETS
- PROJECT_NAME
- AWS_REGION
- AWS_ACCESS_KEY
- AWS_SECRET_KEY
- AWS_S3_BUCKET
- TRACKING_URI
- BASIC_PWD_AUTH # password for mlflow access from nginx home page

```bash
# Set HF_BE_SERVER in .env to match <BACKEND-SERVER-ML-DEPLMT-TEMPL> name
nano .env
HF_BE_SERVER=<BACKEND-SERVER-ML-DEPLMT-TEMPL>
# Create and push backend server
make push SERVER=be MSG="Initial commit"
```
[⬆ Back to top](#table-of-contents)


