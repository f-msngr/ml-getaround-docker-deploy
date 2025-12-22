<img src='assets/screenshots/getaround_logo.png' alt='Getaround logo' width='400'>

# GetAround 

# GetAround - MLOps Deployment Framework

> **3-phase Docker deployment template (local → predeploy → cloud) demonstrating 
> production-grade MLOps architecture on a rental optimization business case.**

[Table of contents](#table-of-contents)

---
# Table of Contents

- [GetAround](#getaround)
- [GetAround - MLOps Deployment Framework](#getaround---mlops-deployment-framework)
- [Table of Contents](#table-of-contents)
  - [🎯 About](#-about)
  - [🎯 Project Goals](#-project-goals)
  - [Tech Stack ⚙️](#tech-stack-️)
  - [ML project framework 🧩](#ml-project-framework-)
  - [Preview](#preview)
  - [Key Features ✨](#key-features-)
  - [Architecture Overview](#architecture-overview)
  - [Requirements 📋](#requirements-)
  - [Project docs 📚](#project-docs-)
- [Getting Started 🚀](#getting-started-)
- [Contributing 🤝](#contributing-)
- [License 📜](#license-)
  - [🎓 Portfolio Context](#-portfolio-context)


## 🎯 About
**Business context** (2-3 lignes seulement) :
GetAround rental delays impact user satisfaction and revenue. This project implements 
ML-based delay prediction and threshold optimization.

**Technical focus** :
Production-ready MLOps template showcasing:
- 3-phase deployment workflow (local dev → predeploy validation → HF Spaces)
- Microservices architecture (FastAPI + Streamlit + MLflow + Nginx)
- Reproducible ETL pipelines with experiment tracking

## 🎯 Project Goals
1. **Architecture**: Build reusable multi-container deployment template
2. **MLOps**: Implement complete ML lifecycle (ETL → training → serving → monitoring)
3. **Business**: Predict rental delays and optimize minimum delay thresholds

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

## Preview

<img src='assets/screenshots/preview.png' width='800'>
<img src='assets/screenshots/preview_dashboard_apis.png' width='800'>


**Setup complexity:** 2-4 hours (first time)

## Key Features ✨

**Deployment Framework:**
- 3-phase workflow: `make compose` (local) → `make build` (test) → `make push` (prod)
- Single-port access via Nginx reverse proxy
- Environment-aware configuration (.env switching)

**MLOps Pipeline:**
- Complete ETL with S3 + NeonDB integration
- MLflow experiment tracking
- FastAPI REST endpoints
- Streamlit dashboard

**Code Quality:**
- Modular backend/frontend separation
- Docker Compose orchestration
- Makefile automation
  
[⬆ Back to top](#table-of-contents)

## Architecture Overview
```mermaid
graph LR
    Dev[Developer] --> Local[Local Dev<br/>make compose]
    Local --> PreDeploy[Test Deploy<br/>make build + run]
    PreDeploy --> Prod[Production<br/>make push]
    
    Local -.->|uses| S3[S3 Bucket]
    Local -.->|uses| DB[NeonDB]
    Prod -->|deploys to| HF[HuggingFace<br/>Spaces]
```

**Full details:** [Architecture docs →](docs/01-architecture.md)

[⬆ Back to top](#table-of-contents)


## Requirements 📋

* Linux (bash shell)
* Python 3.8+
* pip
* Docker with Compose V2
* AWS account (for S3 bucket): see more info [Prerequisites](docs/02-prerequisites.md#aws-s3-bucket)
* Database (NeonDB or SQLite): see more info [Prerequisites](docs/02-prerequisites.md#postgresql-database)
* Hugging Face account: see more info [Prerequisites](docs/02-prerequisites.md#huggingface-account)

    [⬆ Back to top](#table-of-contents)

## Project docs 📚

* [Architecture](docs/01-architecture.md) - Project structure, microservices topology, and deployment diagrams
* [Prerequisites](docs/02-prerequisites.md) - Bucket (dataset + artifact root) and tracking uri setup
* [Local development](docs/03-local_development.md) - Howto build and run local development environment (notebooks + docker compose)
* [Pipeline ETL & ML + utils](docs/04-pipeline.md) - Core libraries implemented for the project
* [Deployment](docs/05-deployment.md) - Howto build and run of deployment containers (local predeploy + cloud deploy stages)
    
    [⬆ Back to top](#table-of-contents)

# Getting Started 🚀

**Estimated time:** 2-4 hours (first setup)

1. **Prerequisites** (30-60 min) → [Setup cloud resources](docs/02-prerequisites.md)
2. **Local Development** (30 min) → [Run locally](docs/03-local_development.md)  
3. **Deployment** (60 min) → [Deploy to production](docs/05-deployment.md)

**Or just explore:**
```bash
git clone https://github.com/Fabthenabab/ml-getaround-docker-deploy.git
cd ml-getaround-docker-deploy
make  # See all commands
```

[⬆ Back to top](#table-of-contents)

# Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests.

# License 📜

This project is licensed under the GPL3 License — see the [LICENSE](./LICENSE) file for details.

[⬆ Back to top](#table-of-contents)

## 🎓 Portfolio Context
**Project Type:** MLOps Architecture & Deployment Framework  
**Focus:** Production deployment patterns over ML sophistication

**Demonstrates:**
- Multi-phase deployment workflow design (local → cloud)
- Microservices orchestration (Docker Compose + Nginx)
- MLOps best practices (tracking, serving, monitoring)
- Infrastructure as Code (Makefile automation)
- Cloud deployment (HuggingFace Spaces multi-container)

📚 **Part of [Fab's Data Science Portfolio](https://github.com/fabthenabab)** — 
7 projects covering the full ML lifecycle from research to production.

[⬆ Back to top](#-table-of-contents)