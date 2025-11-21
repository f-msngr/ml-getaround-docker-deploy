<img src='assets/screenshots/getaround_logo.png' alt='Getaround logo' width='500'>

# GetAround 

[GetAround](https://www.getaround.com/?wpsrc=Google+Organic+Search) is the Airbnb for cars. In 2019, they count over 5 million users and about 20K available cars worldwide.

[Table of contents](#table-of-contents)

## Context 

When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

* Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
* Compare fuel levels.
* Measure how many kilometers were driven.

The checkin and checkout of our rentals can be done with three distinct flows:
* **📱 Mobile** rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
* **Connect:** the driver doesn’t meet the owner and opens the car with his smartphone
* **📝 Paper** contract (negligible)

[Table of contents](#table-of-contents)

## Project 🚧

When using Getaround, drivers book cars for a specific time period, but it happens that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the next rental is on the same day : Customer service often reports users unsatisfaction because they have to wait and may need to cancel the rental.

[Table of contents](#table-of-contents)

## Goals 🎯

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

**Our Product Manager still needs to decide:**
* **threshold:** how long should the minimum delay be?
* **scope:** should we enable the feature for all cars?, only Connect cars?

In order to help them make the right decision, they are asking for some data insights:

* Which share of our owner’s revenue would potentially be affected by the feature?
* How many rentals would be affected by the feature depending on the threshold and scope we choose?
* How often are drivers late for the next check-in? How does it impact the next driver?
* How many problematic cases will it solve depending on the chosen threshold and scope?

[Table of contents](#table-of-contents)

---
# Table of Contents

- [GetAround](#getaround)
  - [Context](#context)
  - [Project 🚧](#project-)
  - [Goals 🎯](#goals-)
- [Table of Contents](#table-of-contents)
  - [Tech Stack ⚙️](#tech-stack-️)
  - [ML project framework 🧩](#ml-project-framework-)
  - [Key Features ✨](#key-features-)
  - [Requirements 📋](#requirements-)
- [Project Structure 🌳](#project-structure-)
    - [TL;DR](#tldr)
    - [Detailed structure](#detailed-structure)
    - [Deployment Workflows](#deployment-workflows)
- [Quick Setup 🛠️](#quick-setup-️)
    - [Installation](#installation)
- [Local Development 🏠](#local-development-)
    - [General](#general)
    - [Notebooks](#notebooks)
    - [Local development:](#local-development)
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
- [Contributing 🤝](#contributing-)
- [License 📜](#license-)


## Tech Stack ⚙️

[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)](https://www.linux.org/) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/) [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/) [![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat&logo=nginx&logoColor=white)](https://nginx.org/) [![MLflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=flat&logo=mlflow&logoColor=blue)](https://mlflow.org/) [![NeonDB](https://img.shields.io/badge/NeonDB-00E5FF?style=flat&logo=postgresql&logoColor=white)](https://neon.tech/) [![AWS Cloud](https://img.shields.io/badge/AWS%20Cloud-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/) [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)


## ML project framework 🧩

Develop locally, deploy easily, dockerized production-ready ML deployment template with:
- 🏗️ Microservices architecture (FastAPI + Streamlit + MLflow)
- 🌐 Web interface with nginx reverse proxy for easy access to each service
- 🔄 Complete ETL pipeline
- 🔧 Local development support
- 🚀 One-click deployment to Hugging Face Spaces (with Makefile and env variables)

    [⬆ Back to top](#table-of-contents)
---
## Key Features ✨

* 🛠️ 2 modes: local development or deploy mode selected and launched: by Makefile
* 📦 Modular backend/frontend separation (frontend: visualization and prediction / backend: ETL process)
* 🐳 Dockerized services (nginx, FastAPI, Streamlit, MLflow)
* 🔁 Reproducible ETL pipeline
* ☁️ AWS S3 + NeonDB support
* 🧪 Experiment tracking via MLflow
* 🌐 Single-port deployment via Nginx reverse proxy
* 🤗 Optimized for Hugging Face Spaces multi-service architecture

    [⬆ Back to top](#table-of-contents)
---
## Requirements 📋

* Linux (bash shell)
* Python 3.8+
* pip
* Docker with Compose V2
* AWS account (for S3 bucket)
* Database (NeonDB or SQLite)
* Hugging Face account

    [⬆ Back to top](#table-of-contents)
---
# Project Structure 🌳

### TL;DR 
```
.
├── _CONF                           # specific configuration of servers for deployment on HF Spaces
├── _fastapi-backend-server         # api-backend server configuration                
├── _fastapi-server                 # frontend server configuration
├── _fastapi-servers-shared         # shared route for backend and frontend api (for DRY code purpose)
├── _streamlit-server               # dashboard server configuration
├── _nginx-server                   # reverse proxy server configuration
├── _mlflow-server                  # mlflow server configuration
├── data                            # use for local dev
├── pipeline                        # src dir for etl and train processing and general & reusable src
├── models                          # use for local dev - switch to Artifact store in deployment
├── metrics                         # use for local dev - switch to Backend store in deployment
└── notebooks                       # local use, dev, and general test purposes
```

[⬆ Back to top](#table-of-contents)

### Detailed structure
<details>
<summary>🌳 Detailed structure (click to expand)</summary>

    .
    ├── _CONF                           # backend & frontend services configuration for <u>deployment on HF Spaces</u>
    │   └── deploy
    │       ├── backend_deploy_dir
    │       │   ├── nginx/              # nginx backend server configuration (home page + reverse proxy service configuration)
    │       │   ├── Dockerfile          # nginx, api-backend, pipeline files, env variables import, ...
    │       │   ├── requirements.txt
    │       │   └── start.sh            # run script: api-backend + nginx
    │       └── frontend_deploy_dir
    │           ├── nginx/              # nginx frontend server configuration (different home page, different API)
    │           ├── Dockerfile          # nginx, streamlit, api, pipeline files, env variables import, ...
    │           ├── requirements.txt
    │           └── start.sh            # run script: streamlit + api + nginx
    ├── _fastapi-backend-server         # api-backend server configuration + src
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src
    │       ├── fastapi.py              # use of routes to separate functional parts)
    │       ├── route_auth.py           # authentification route with cookie setting and checking (dummy hard coded pwd only for POC)
    │       ├── route_extract.py        # extraction route (dummy deserialization from AWS S3 Bucket) - to be replaced by a real one
    │       ├── route_train.py          # train route (random forest classifier for POC) - to be replaced
    │       ├── route_transform.py      # tranform route (dummy column tranformation in dataset for POC) - to be replaced
    │       └── shared                  
    ├── _fastapi-server                 # frontend server configuration + src
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src
    │       ├── fastapi.py
    │       └── shared
    ├── _fastapi-servers-shared         # shared route: routes that are shared by backend and frontend api (for DRY code purpose)
    │   └── src
    │       ├── route_load.py
    │       └── route_predict.py
    ├── _streamlit-server               # dashboard server configuration
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src
    │       └── streamlit.py            # only for display reason - calls api whenever possible
    ├── _nginx-server                   # reverse proxy server configuration. Redirect incoming requests on every listening service
    │   ├── default.conf.templ          # contains PORTS defined as .env variables. File modified by make compose and copied to default.conf
    │   └── html
    │       ├── img
    │       └── index.html
    ├── _mlflow-server                  # mlflow server orchestration configuration dir
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── run.sh
    ├── assets                          # project documentation purpose
    │   └── screenshots
    ├── data                            # use for local dev - mounted as a volume - switch to mlflow in deployment
    │   ├── processed
    │   └── raw
    │       └── iris.csv                # dummy raw tabular data file
    ├── pipeline                        # src dir for etl and train processing and general & reusable src (aws connection, )
    │   ├── core
    │   │   ├── src
    │   │   │   ├── extract.py
    │   │   │   ├── load.py
    │   │   │   ├── predict.py
    │   │   │   └── train.py
    │   │   └── tests
    │   └── libs
    │       ├── src
    │       │   ├── aws.py
    │       │   └── utils.py
    │       └── tests
    ├── models                          # use for local dev - mounted as a volume - switch to Artifact store (S3) in deployment
    ├── metrics                         # use for local dev - mounted as a volume - switch to Backend store (Postgres/NeonDB) in deployment
    ├── notebooks                       # local use, dev, and general test purposes. Left here as sandboxes
    │   ├── Dummy.ipynb                 # local tests notebook - may use data/ metrics/ or models/
    │   ├── EDA.ipynb
    │   ├── ETL.ipynb
    │   └── train.ipynb
    ├── docker-compose.yml              # defines the different services that are launched by Makefile (make compose)
    ├── Makefile                        # switch to compose (local dev) or deploy mode -> read file doc
    └── .env                            # env files to be completed with private keys - Need also to be set as SECRETS in HF Spaces

</details>

[⬆ Back to top](#table-of-contents)


### Deployment Workflows

<details>
<summary>🏠 Local development (click to expand)</summary>

```mermaid
flowchart TB
    %% filesystem
    subgraph filesystem["filesystem"]
        subgraph servers["servers"]
            nginxserver["_nginx-server"]
            streamlitserver["_streamlit-server"]
            fastapiserversshared["_fastapi-servers-shared"]
            fastapiserver["_fastapi-server"]
            fastapibackendserver["_fastapi-backend-server"]
            mlflowserver["_mlflow-server"]
        end
        dockercompose["docker-compose.yml"]
        subgraph volumes["bind mount volumes"]
            data[data]
            metrics[metrics]
            models[models]
            pipeline[pipeline]
        end
    end
    
    %% Makefile
    subgraph makefile["Makefile"]
        compose{"compose"}
    end

    %% compose
    servers --> compose
    dockercompose --> compose
    
    subgraph dockernetwork["docker network"]
        nginxcontainer["nginx container"]
        streamlitcontainer["dashboard container"]
        apicontainer["api container"]
        apibackendcontainer["api-backend container"]
        mlflowcontainer["mlflow-tracking container"]
    end
    nginxcontainer --> streamlitcontainer
    nginxcontainer --> apicontainer
    nginxcontainer --> apibackendcontainer
    nginxcontainer --> mlflowcontainer

    compose --> dockernetwork
    servers -.->|bind mount| dockernetwork
    volumes <-.->|bind mount| dockernetwork
```
</details>

[⬆ Back to top](#table-of-contents)

<details>
<summary>🏗️ Local predeployment (click to expand)</summary>

```mermaid
flowchart TB
    %% filesystem
    subgraph filesystem["filesystem"]
        servers["servers"]
        pipeline[pipeline]
        conf[_CONF]
        subgraph predeploydir["Predeployment dir"]
            frontenddeploydir[frontend_deploy_dir]
            backenddeploydir[backend_deploy_dir]
            mlflowdeploydir[mlflow_deploy_dir]
        end
    end
    
    %% Makefile
    subgraph makefile["Makefile"]
        build{"build"}
        run{"run"}
    end

    %% build
    conf --> build
    servers --> build
    pipeline --> build
    build --> predeploydir

 
    %% run
    subgraph localpredeploycontainer["Local environment"]
        subgraph frontendlocalpredeploycontainer["frontend container"]
            frontendnginx["nginx"]
            frontendstreamlit["streamlit"]
            frontendfastapi["fastapi frontend"]
            frontendstreamlit --> frontendfastapi
        end
        subgraph backendlocalpredeploycontainer["backend container"]
            backendnginx["nginx"]
            backendfastapi["fastapi backend"]
        end
    end
    frontendnginx --> frontendstreamlit
    frontendnginx --> frontendfastapi
    backendnginx --> backendfastapi
    subgraph mlflowdeployedcontainer["Hugging Face Spaces"]
        hfdeployedmlflow["mlflow"]
    end
    backendnginx --> hfdeployedmlflow
    
    predeploydir --> run
    run --> localpredeploycontainer
    db[("Backend Store - NeonDB")]
    bucket[("Artifact Store - S3 Bucket")]

    frontendfastapi --> bucket
    backendfastapi --> bucket 
    hfdeployedmlflow --> bucket
    hfdeployedmlflow --> db

```
</details>

[⬆ Back to top](#table-of-contents)

<details>
<summary>🤗 Hugging Face Spaces deployment (click to expand)</summary>

```mermaid
flowchart TB
    %% filesystem
    subgraph filesystem["filesystem"]
        subgraph predeploydir["Predeployment dir"]
            frontenddeploydir[frontend_deploy_dir]
            backenddeploydir[backend_deploy_dir]
            mlflowdeploydir[mlflow_deploy_dir]
        end
        subgraph hfspaces["_HF_SPACES"]
            frontendpushdir["HF frontend container"]
            backendpushdir["HF backend container"]
            mlflowpushdir["HF mlflow container"]
        end
    end
    
    %% Makefile
    subgraph makefile["Makefile"]
        push{"push"}
    end


    %% push
    subgraph mlflowdeployedcontainer["Hugging Face Spaces"]
        hfdeployedfrontend["frontend"]
        hfdeployedbackend["backend"]
        hfdeployedmlflow["mlflow"]
    end
    frontenddeploydir --> push
    backenddeploydir --> push
    mlflowdeploydir --> push

    push --> frontendpushdir
    push --> backendpushdir
    push --> mlflowpushdir

    frontendpushdir --> hfdeployedfrontend
    backendpushdir --> hfdeployedbackend
    mlflowpushdir  --> hfdeployedmlflow

    db[("Backend Store - NeonDB")]
    bucket[("Artifact Store - S3 Bucket")]

    hfdeployedfrontend --> bucket
    hfdeployedbackend --> bucket 
    hfdeployedmlflow --> bucket
    hfdeployedmlflow --> db

```
</details>

[⬆ Back to top](#table-of-contents)

---
# Quick Setup 🛠️

### Installation

```bash
# Check Docker installation
docker --version
docker compose version

# Go to parent cloning directory
mkdir YOUR_PARENT_CLONING_DIR

# Clone the project
git clone https://github.com/Fabthenabab/ml-getaround-docker-deploy.git
cd ml-getaround-docker-deploy
```

Open your existing <AWS_S3_BUCKET> in your your AWS S3 manager (as $AWS_S3_BUCKET)  
(If you don't have any existing bucket, create one)  
Create new <PROJECT_NAME> folder in <AWS_S3_BUCKET> (will match $PROJECT_NAME in .env)  

```bash
# Edit and rename .env.example to .env to fit your configuration and credentials
mv .env.example .env
nano .env
# Set values 
#   - PROJECT_NAME
#   - AWS_REGION
#   - AWS_ACCESS_KEY
#   - AWS_SECRET_KEY
#   - AWS_S3_BUCKET
#   - ARTIFACT_ROOT
```

[⬆ Back to top](#table-of-contents)


---
# Local Development 🏠

### General

The support dataset is accessible on the S3 bucket.  

⚠️ For this project, the dashboard and the underlying api need some files in S3 (by default).

Run `make compose`  
Open browser and execute the extract, load, train, .. actions via the swagger interface.



Used files:

    .
    └── data                          
        ├── raw
        │   ├── df_rentals.pkl          # rentals dataframe
        │   └── df_cars.pkl             # cars dataframe
        └── transformed                          
            └── df_cars_transformed.pkl   # transformed dataset)


[⬆ Back to top](#table-of-contents)

### Notebooks  

Use your Python environment (`.venv-YOUR_VIRTUAL_ENV_NAME`) with `ipykernel` support for notebooks.

```bash
# Follow above Local development steps
# Allow use of jupyter notebooks
pip install jupyter ipykernel
```

Use notebooks in `notebooks` to run:
- from `notebooks/EDA.ipynb`, `notebooks/ETL.ipynb`, `notebooks/train.ipynb`



Create New PostGRESQL Database (use of NeonDB here)  

<img src='assets/screenshots/NeonDB_project_creation.png' alt='NeonDB_new_db_creation' width='500'>

```bash
# Set connection string to your new database given by the db manager console 
#   - BACKEND_STORE_URI=<CONNECTION_STRING_TO_THE_NEWLY_CREATED_DB>
```

```bash
# Local dev compose command will run docker compose build and docker compose up (see Makefile compose)
make compose
```

Open interface in browser with port `$PORT_NGINX_EXTERNAL` defined in .env (default port: 8088)  
`http://localhost:8088/`

<img src='assets/screenshots/home_local_dev.png' alt='local dev home page' width='500'>

[⬆ Back to top](#table-of-contents)

### Local development:
In local development, some services rely on bind-mounted volumes (e.g. `data/`, `metrics/`, `models/`) to make testing and rapid iteration easier. These volumes allow artifacts, metrics, and logs generated by the microservices to be stored locally, all served through an Nginx reverse proxy.

Servers volumes containing code to edit should be also mounted as bound volumes. See docker-compose.yml for more information.

```bash
# To develop locally
# Create and activate a virtual environment (optional)
python -m venv .venv-YOUR_VIRTUAL_ENV_NAME
source .venv-YOUR_VIRTUAL_ENV_NAME/bin/activate
# Install dependencies (adjust if needed)
pip install --upgrade pip
pip install -r _fastapi-backend-server/requirements.txt
pip install -r _fastapi-server/requirements.txt
pip install -r _mlflow-server/requirements.txt
pip install -r _streamlit-server/requirements.txt
```
⚠️ you may need to restart the servers services with `make compose` process to refresh the src that are copied during build time

[⬆ Back to top](#table-of-contents)





--------------------------------------------------------------------------------------------------------


---
# Local Pre deployment 🏗️

### Build

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
<img src='assets/screenshots/home_local_deploy_frontend.png' alt='local deploy_frontend home page' width='300'>  

Open backend interface in browser with port ```$PORT_REV_PROXY_BACKEND_EXTERNAL``` defined in .env (default port: 7861):  
`http://localhost:7861/`  
<img src='assets/screenshots/home_local_deploy_backend.png' alt='local deploy_backend home page' width='300'>

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

---
# HuggingFace Spaces deployment 🤗

Create New Blank Public Docker Space for each server on HF Space

### MLFlow Server space

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

### Frontend Server space

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

### Backend Server space

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

---
# Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests.

# License 📜

This project is licensed under the GPL3 License — see the [LICENSE](./LICENSE) file for details.

[⬆ Back to top](#table-of-contents)