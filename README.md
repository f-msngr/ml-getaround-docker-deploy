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
  - [Project docs 📚](#project-docs-)
- [Quick Setup 🛠️](#quick-setup-️)
    - [Installation](#installation)
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

## Key Features ✨

* 🛠️ 2 modes: local development or deploy mode selected and launched: by Makefile
* 📦 Modular backend/frontend separation (frontend: visualization and prediction / backend: ETL process)
* 🐳 Dockerized services (nginx, FastAPI, Streamlit, MLflow)
* 🔁 Reproducible ETL pipeline
* ☁️ AWS S3 + NeonDB support
* 🧪 Experiment tracking via MLflow
* 🌐 Single-port deployment via Nginx reverse proxy
* 🤗 Optimized for Hugging Face Spaces multi-services architecture

    [⬆ Back to top](#table-of-contents)

## Requirements 📋

* Linux (bash shell)
* Python 3.8+
* pip
* Docker with Compose V2
* AWS account (for S3 bucket): see more info [Prerequisites](docs/02-prerequisites.md)
* Database (NeonDB or SQLite): see more info [Prerequisites](docs/02-prerequisites.md)
* Hugging Face account: see more info [Prerequisites](docs/02-prerequisites.md)

    [⬆ Back to top](#table-of-contents)

## Project docs 📚

* [Architecture](docs/01-architecture.md) - Project structure, microservices topology, and deployment diagrams
* [Prerequisites](docs/02-prerequisites.md) - Bucket (dataset + artifact root) and tracking uri setup
* [Local development](docs/03-local_development.md) - Howto build and run local development environment (notebooks + docker compose)
* [Pipeline ETL & ML + utils](docs/04-pipeline.md) - Core libraries implemented for the project
* [Deployment](docs/05-deployment.md) - Howto build and run of deployment containers (local predeploy + cloud deploy stages)
    
    [⬆ Back to top](#table-of-contents)

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
Setup your bucket. More information in [Prerequisites](docs/02-prerequisites.md)

[⬆ Back to top](#table-of-contents)


# Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests.

# License 📜

This project is licensed under the GPL3 License — see the [LICENSE](./LICENSE) file for details.

[⬆ Back to top](#table-of-contents)