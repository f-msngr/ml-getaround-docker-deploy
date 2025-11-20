.DEFAULT_GOAL := help

# Import .env variables
include .env
export

DEPLOY_CONF_DIR=_CONF/deploy

PIPELINE_DIR=pipeline
LIBS_DIR=$(PIPELINE_DIR)/libs
CORE_DIR=$(PIPELINE_DIR)/core
PROCESS_DIR=$(PIPELINE_DIR)/process
APIS_SHARED_DIR=_fastapi-servers-shared/src

# SET LOCAL VARIABLES
REV_PROXY_DIR=_nginx-server
REV_PROXY_DIR_DEST=nginx
REV_PROXY_ALT_DEPLOY=ALT_DEPLOY

# Frontend Deploy Dir
FRONTEND_DEPLOY_DIR=frontend_deploy_dir
DASHBOARD_DIR=_streamlit-server
API_DIR_SRC=_fastapi-server
API_DIR_DEST=api
FRONTEND_IMAGE=frontend_image-templ

# Backend Deploy Dir
BACKEND_DEPLOY_DIR=backend_deploy_dir
API_BACKEND_DIR_SRC=_fastapi-backend-server
API_BACKEND_DIR_DEST=api-backend
BACKEND_IMAGE=backend_image-templ

# MLFlow Deploy Dir
MLFLOW_DEPLOY_DIR=mlflow_deploy_dir
MLFLOW_DIR_SRC=_mlflow-server
MLFLOW_DEPLOY_IMAGE=mlflow_image-templ

HFSPACES_DEPLOY_DIR=_HF-SPACES

.PHONY: deploy build clean

##########################################################################################################################
##########                    LOCAL DEV                                                                         ##########
##########################################################################################################################
compose:
# Build and Run services defined in ./docker-compose.yml
# Use service/Dockerfile and service/requirements
# Use ./.env
	@echo "🚀 COMPOSING AND BUILDING LOCAL SERVICES IN CONTAINERS"
	@docker compose down \
		&& echo " => Stopping containers: ✅"
	@docker rm -f $(STREAMLIT_CONTAINER) \
		&& docker rmi -f $(STREAMLIT_IMAGE) \
		&& echo " => Removed container $(STREAMLIT_CONTAINER) and image $(STREAMLIT_IMAGE): ✅"
	@docker rm -f $(FASTAPI_CONTAINER) \
		&& docker rmi -f $(FASTAPI_IMAGE) \
		&& echo " => Removed container $(FASTAPI_CONTAINER) and image $(FASTAPI_IMAGE): ✅"
	@docker rm -f $(FASTAPI_BACKEND_CONTAINER) \
		&& docker rmi -f $(FASTAPI_BACKEND_IMAGE) \
		&& echo " => Removed container $(FASTAPI_BACKEND_CONTAINER) and image $(FASTAPI_BACKEND_IMAGE): ✅"
	@docker rm -f $(MLFLOW_CONTAINER) \
		&& docker rmi -f $(MLFLOW_IMAGE) \
		&& echo " => Removed container $(MLFLOW_CONTAINER) and image $(MLFLOW_IMAGE): ✅"
	@docker rm -f $(NGINX_CONTAINER) \
		&& echo " => Removed container $(NGINX_CONTAINER): ✅"
	@docker image prune -f \
		&& echo " => Removed dangling images: ✅"

	@echo "Stopping containers listening on port $$PORT_MLFLOW_TRACKING_EXTERNAL..."
	@containers=$$(docker ps --filter "publish=$$PORT_MLFLOW_TRACKING_EXTERNAL" --format "{{.Names}}"); \
	if [ -z "$$containers" ]; then \
		echo "No running MLflow containers found on port $$PORT_MLFLOW_TRACKING_EXTERNAL"; \
	else \
		echo "Found MLflow containers:"; \
		echo "$$containers"; \
		echo "$$containers" | xargs -n1 docker rm -f; \
		echo "Containers removed ✅"; \
	fi

# Replace port values by their value defined in .env in _nginx-server/default.conf.templ
# Create _nginx-server/default.conf from it
	@echo "Replacing port value nginx configuration file"
	@echo " => Generating nginx configuration from template"
	@envsubst '$${PORT_NGINX_EXTERNAL} \
				$${PORT_STREAMLIT_EXTERNAL} \
				$${PORT_FASTAPI_EXTERNAL} \
				$${PORT_FASTAPI_BACKEND_EXTERNAL} \
				$${PORT_MLFLOW_TRACKING_EXTERNAL}' \
				< $(REV_PROXY_DIR)/default.conf.templ > $(REV_PROXY_DIR)/default.conf
	@echo " => Created $(REV_PROXY_DIR)/default.conf: ✅"

	@docker compose build --no-cache \
		&& echo " => Building without cache from last version of base image: ✅"
#	ADD -d to have running detached containers
#	@docker compose up -d --force-recreate \
		&& echo " => Running containers recreated: ✅"
	@docker compose up --force-recreate \
		&& echo " => Application stopped: 🛑"

##########################################################################################################################
##########                    LOCAL DEPLOY                                                                      ##########
##########################################################################################################################

deploy:
# Create local dir and sub dirs for deployment
# First for local deployment as a test
# Ready to be commited on Hugging Face
# Will use 2 images and therefore 2 deployments on HF
# make deploy is called by make build
# First: Create Front End Deploy Dir (dashboard + api/ reverse proxy)
	@echo "🚀 CREATING FRONTEND DEPLOYMENT DIR"
	@rm -rf $(FRONTEND_DEPLOY_DIR) \
		&& echo " => Removing $(FRONTEND_DEPLOY_DIR): ✅"

	@echo "[FRONTEND DEPLOY DIR]"
	@mkdir -p $(FRONTEND_DEPLOY_DIR)
	@echo "Directory $(FRONTEND_DEPLOY_DIR) automatically created for deployment on Hugging Face by makefile. Conf files from $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)" > $(FRONTEND_DEPLOY_DIR)/README.txt 

	@echo "[API]"
	@mkdir -p $(FRONTEND_DEPLOY_DIR)/$(API_DIR_DEST)
	@cp -r $(API_DIR_SRC)/src/ $(FRONTEND_DEPLOY_DIR)/$(API_DIR_DEST)
	@touch $(FRONTEND_DEPLOY_DIR)/$(API_DIR_DEST)/__init__.py
# Copy local shared libraries (routes) to duplicate them in each deploy directory (frontend dir)
	@rsync -a $(APIS_SHARED_DIR)/ $(FRONTEND_DEPLOY_DIR)/$(API_DIR_DEST)/src/shared/

	@echo "[DASHBOARD]"
	@mkdir -p $(FRONTEND_DEPLOY_DIR)/streamlit
	@cp -r $(DASHBOARD_DIR)/src/ $(FRONTEND_DEPLOY_DIR)/streamlit
	@cp -r $(DASHBOARD_DIR)/.streamlit/ $(FRONTEND_DEPLOY_DIR)/streamlit
	@cp -r $(DASHBOARD_DIR)/README.txt $(FRONTEND_DEPLOY_DIR)/streamlit
	

	@echo "[REVERSE PROXY]"
# copy _nginx-server/html + README.txt
# replace deploy_dir/nginx/html/index.html with _CONF/deploy/nginx/html/index.html
# copy _CONF default.conf + hot modification of port mapping according to .env values
	@mkdir -p $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)
	@rsync -a $(REV_PROXY_DIR)/html/* $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/ \
		&& echo " => Copying $(REV_PROXY_DIR)/html: ✅"
	@rsync -a $(REV_PROXY_DIR)/README.txt $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/ \
		&& echo " => Copying $(REV_PROXY_DIR)/README.txt: ✅"
	@rsync -a $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/index.html $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/index.html \
		&& echo " => Copying $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/index.html: ✅"
	@echo " => Generating $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf with .env port mapping"
	@envsubst '$${PORT_REV_PROXY_FRONTEND_EXTERNAL} $${PORT_FASTAPI_EXTERNAL} $${PORT_STREAMLIT_EXTERNAL}' < $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf > $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf
	@echo " => Updated $(FRONTEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf: ✅"

	@echo "[PIPELINE]"
	@mkdir -p $(FRONTEND_DEPLOY_DIR)/$(PIPELINE_DIR)
	@cp -r $(PIPELINE_DIR)/ $(FRONTEND_DEPLOY_DIR)/ \
		&& echo " => Copying pipeline utils lib files: ✅"

	@echo "[REQUIREMENTS]"
	@cp $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/requirements.txt $(FRONTEND_DEPLOY_DIR)

	@echo "[STARTING SCRIPT]"
# Replace PORT_FASTAPI_EXTERNAL and PORT_STREAMLIT_EXTERNAL by their value in $(FRONTEND_DEPLOY_DIR)/start.sh
	@echo " => Copying and Modifying $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/start.sh .env port mapping"
	@envsubst '$${PORT_FASTAPI_EXTERNAL} $${PORT_STREAMLIT_EXTERNAL}' < $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/start.sh > $(FRONTEND_DEPLOY_DIR)/start.sh
	@echo " => Copied and Modified $(FRONTEND_DEPLOY_DIR)/start.sh: ✅"


	@echo "[DOCKERFILE]"
# Replace PORT_REV_PROXY_FRONTEND_EXTERNAL + PORT_REV_PROXY_FRONTEND_EXPOSED by their value in $(FRONTEND_DEPLOY_DIR)/Dockerfile
	@echo " => Copying and Modifying $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/Dockerfile .env port mapping"
	@envsubst '$${PORT_REV_PROXY_FRONTEND_EXTERNAL} $${PORT_REV_PROXY_FRONTEND_EXPOSED}' < $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/Dockerfile > $(FRONTEND_DEPLOY_DIR)/Dockerfile
	@echo " => Copied and Modified $(FRONTEND_DEPLOY_DIR)/Dockerfile: ✅"
	@cp $(DEPLOY_CONF_DIR)/$(FRONTEND_DEPLOY_DIR)/.dockerignore $(FRONTEND_DEPLOY_DIR)/

	@echo "🧹 [CLEANING $(FRONTEND_DEPLOY_DIR)]"
	@find $(FRONTEND_DEPLOY_DIR) -type d -name '__pycache__' -exec rm -rf {} + \
		&& echo "=> Removing __pycache__ in $(FRONTEND_DEPLOY_DIR): ✅"

	@echo " => FRONTEND DEPLOY DIR: ✅"
	@echo "🌳 FRONTEND DEPLOY DIR STRUCTURE"
	@if command -v tree >/dev/null 2>&1; then \
		tree -L 3 $(FRONTEND_DEPLOY_DIR); \
	else \
		echo "⚠️ tree unavailable, fallback to ls -al :"; \
		ls -al $(FRONTEND_DEPLOY_DIR); \
	fi

# Second: Create Backend Deployment dir (nginx, fastapi, pipeline)
	@echo "🚀 CREATING BACKEND DEPLOYMENT DIR"
	@rm -rf $(BACKEND_DEPLOY_DIR) \
		&& echo " => Removing $(BACKEND_DEPLOY_DIR): ✅"

	@echo "[BACKEND DEPLOY DIR]"
	@mkdir -p $(BACKEND_DEPLOY_DIR)
	@echo "Directory $(BACKEND_DEPLOY_DIR) automatically created for deployment on Hugging Face by makefile. Conf files from $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)" > $(BACKEND_DEPLOY_DIR)/README.txt 


	@echo "[API BACKEND]"
	@mkdir -p $(BACKEND_DEPLOY_DIR)/$(API_BACKEND_DIR_DEST)
	@cp -r $(API_BACKEND_DIR_SRC)/src/ $(BACKEND_DEPLOY_DIR)/$(API_BACKEND_DIR_DEST)
	@touch $(BACKEND_DEPLOY_DIR)/$(API_BACKEND_DIR_DEST)/__init__.py
# Copy local shared libraries (routes) to duplicate them in each deploy directory (backend dir)
	@rsync -a $(APIS_SHARED_DIR)/ $(BACKEND_DEPLOY_DIR)/$(API_BACKEND_DIR_DEST)/src/shared/

	@echo "[REVERSE PROXY]"
# copy _nginx-server/html + README.txt
# replace deploy_dir/nginx/html/index.html with _CONF/deploy/nginx/html/index.html
# copy _CONF default.conf + hot modification of port mapping according to .env values
	@mkdir -p $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)
	@rsync -a $(REV_PROXY_DIR)/html/* $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/ \
		&& echo " => Copying $(REV_PROXY_DIR)/html: ✅"
	@rsync -a $(REV_PROXY_DIR)/README.txt $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/ \
		&& echo " => Copying $(REV_PROXY_DIR)/README.txt: ✅"
	@rsync -a $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/index.html $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/index.html \
		&& echo " => Copying $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/html/index.html: ✅"
	@echo " => Generating $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf with .env port mapping"
	@envsubst '$${PORT_REV_PROXY_BACKEND_EXTERNAL} $${PORT_FASTAPI_BACKEND_EXTERNAL} $${MLFLOW_PROXY_PASS}' < $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf > $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf
	@echo " => Updated $(BACKEND_DEPLOY_DIR)/$(REV_PROXY_DIR_DEST)/default.conf: ✅"

	
	@echo "[PIPELINE]"
	@mkdir -p $(BACKEND_DEPLOY_DIR)/$(PIPELINE_DIR)
	@cp -r $(PIPELINE_DIR)/ $(BACKEND_DEPLOY_DIR)/ \
		&& echo " => Copying pipeline files: ✅"

	@echo "[DOCKERFILE]"
# Replace PORT_FASTAPI_BACKEND_EXPOSED + PORT_REV_PROXY_BACKEND_EXPOSED by their value in $(BACKEND_DEPLOY_DIR)/Dockerfile
	@echo " => Copying and Modifying $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/Dockerfile .env port mapping"
	@envsubst '$${PORT_FASTAPI_BACKEND_EXPOSED} $${PORT_REV_PROXY_BACKEND_EXPOSED}' < $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/Dockerfile > $(BACKEND_DEPLOY_DIR)/Dockerfile
	@echo " => Copied and Modified $(BACKEND_DEPLOY_DIR)/Dockerfile: ✅"
	@cp $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/.dockerignore $(BACKEND_DEPLOY_DIR)/

	@echo "[REQUIREMENTS]"
	@cp -r $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/requirements.txt $(BACKEND_DEPLOY_DIR)/

	@echo "🧹 [CLEANING $(BACKEND_DEPLOY_DIR)]"
	@find $(BACKEND_DEPLOY_DIR) -type d -name '__pycache__' -exec rm -rf {} + \
		&& echo "=> Removing __pycache__ in $(BACKEND_DEPLOY_DIR): ✅"

	@echo "[STARTING SCRIPT]"
# Replace PORT_FASTAPI_BACKEND_EXPOSED by its value in $(BACKEND_DEPLOY_DIR)/start.sh
	@echo " => Copying and Modifying $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/start.sh .env port mapping"
	@envsubst '$${PORT_FASTAPI_BACKEND_EXPOSED}' < $(DEPLOY_CONF_DIR)/$(BACKEND_DEPLOY_DIR)/start.sh > $(BACKEND_DEPLOY_DIR)/start.sh
	@echo " => Copied and Modified $(BACKEND_DEPLOY_DIR)/start.sh: ✅"

	@echo " => BACKEND DEPLOY DIR: ✅"
	
	@echo "🌳 BACKEND DEPLOY DIR STRUCTURE"
	@if command -v tree >/dev/null 2>&1; then \
		tree -L 3 $(BACKEND_DEPLOY_DIR); \
	else \
		echo "⚠️ tree unavailable, fallback to ls -al :"; \
		ls -al $(BACKEND_DEPLOY_DIR); \
	fi

# Third: Create MLFlow Deployment dir (ml tracking)
	@echo "🚀 CREATING MLFLOW DEPLOYMENT DIR"
	@rm -rf $(MLFLOW_DEPLOY_DIR) \
		&& echo " => Removing $(MLFLOW_DEPLOY_DIR): ✅"

	@echo "[MLFLOW]"
	@mkdir -p $(MLFLOW_DEPLOY_DIR)
	@rsync -a $(MLFLOW_DIR_SRC)/* $(MLFLOW_DEPLOY_DIR)/ \
		&& echo " => Copying MLFlow files $(MLFLOW_DIR_SRC): ✅"
	
	@echo " => Modifying $(MLFLOW_DEPLOY_DIR)/run.sh and $(MLFLOW_DEPLOY_DIR)/Dockerfile with .env port mapping"
# Modify Local port mapping for development with docker-compose.yml multiservices under docker network to HF default port (7860)
# Modify run.sh + Dockerfile
	@sed -i 's/PORT_MLFLOW_TRACKING_EXTERNAL/PORT_MLFLOW_HF_DEPLOYED_DEFAULT/g' $(MLFLOW_DEPLOY_DIR)/run.sh
	@envsubst '$${PORT_MLFLOW_HF_DEPLOYED_DEFAULT}' < $(MLFLOW_DEPLOY_DIR)/run.sh > $(MLFLOW_DEPLOY_DIR)/run.sh.tmp
	@mv $(MLFLOW_DEPLOY_DIR)/run.sh.tmp $(MLFLOW_DEPLOY_DIR)/run.sh
	@sed -i 's/PORT_MLFLOW_TRACKING_EXTERNAL/PORT_MLFLOW_HF_DEPLOYED_DEFAULT/g' $(MLFLOW_DEPLOY_DIR)/Dockerfile
	@envsubst '$${PORT_MLFLOW_HF_DEPLOYED_DEFAULT}' < $(MLFLOW_DEPLOY_DIR)/Dockerfile > $(MLFLOW_DEPLOY_DIR)/Dockerfile.tmp
	@mv $(MLFLOW_DEPLOY_DIR)/Dockerfile.tmp $(MLFLOW_DEPLOY_DIR)/Dockerfile
	@echo " => Updated $(MLFLOW_DEPLOY_DIR)/Dockerfile: ✅"

	@echo " => MLFLOW DEPLOY DIR: ✅"
	
	@echo "🌳 MLFLOW DEPLOY DIR STRUCTURE"
	@if command -v tree >/dev/null 2>&1; then \
		tree -L 3 $(MLFLOW_DEPLOY_DIR); \
	else \
		echo "⚠️ tree unavailable, fallback to ls -al :"; \
		ls -al $(MLFLOW_DEPLOY_DIR); \
	fi

build: deploy
# Build Frontend Image, Backend Image, MLFlow Image
# Build image with:
# ./Dockerfile
# ./requirements 
# ./start.sh
	@echo "🗑️ REMOVING RUNNING CONTAINERS FROM PREVIOUS make compose USE (images names dc-... as defined in .env)"
	@echo " => Running containers services from previous make compose"
	@count=$$(docker ps --filter "name=^dc-" --format "{{.Names}}" | wc -l | xargs); \
	if [ "$$count" -eq 0 ]; then \
		echo "    0 running containers"; \
	else \
		docker ps --filter "name=^dc-" --format "{{.Names}}"; \
	fi
	@docker compose down \
		&& docker ps --filter "name=^dc-" --format "{{.Names}}" \
		&& echo " => Containers removed: ✅"

	@echo " => Stopping containers listening on port $$PORT_MLFLOW_TRACKING_EXTERNAL... as defined in .env"
	@containers=$$(docker ps --filter "publish=$$PORT_MLFLOW_TRACKING_EXTERNAL" --format "{{.Names}}"); \
	if [ -z "$$containers" ]; then \
		echo "    No running MLflow containers found on port $$PORT_MLFLOW_TRACKING_EXTERNAL"; \
	else \
		echo "    Found MLflow containers:"; \
		echo "    $$containers"; \
		echo "    $$containers" | xargs -n1 docker rm -f; \
		echo " => Containers removed: ✅"; \
	fi
	
	@echo "🚀 BUILDING DEPLOYMENT IMAGES"
	@docker build -t $(FRONTEND_IMAGE) ./$(FRONTEND_DEPLOY_DIR) \
		&& echo " => Built image $(FRONTEND_IMAGE): ✅"
	@docker build -t $(BACKEND_IMAGE) ./$(BACKEND_DEPLOY_DIR) \
		&& echo " => Built image $(BACKEND_IMAGE): ✅"
	@docker build -t $(MLFLOW_DEPLOY_IMAGE) ./$(MLFLOW_DEPLOY_DIR) \
		&& echo " => Built image $(MLFLOW_DEPLOY_IMAGE): ✅"


stop:
	@echo "🛑 STOPPING $(MLFLOW_DEPLOY_IMAGE)-container"
	@docker stop $(MLFLOW_DEPLOY_IMAGE)-container > /dev/null 2>&1 || true \
		&& docker rm $(MLFLOW_DEPLOY_IMAGE)-container > /dev/null 2>&1 || true \
		&& echo " => $(MLFLOW_DEPLOY_IMAGE)-container stopped and removed: ✅"

	@echo "🛑 STOPPING $(FRONTEND_IMAGE)-container"
	@docker stop $(FRONTEND_IMAGE)-container > /dev/null 2>&1 || true \
		&& docker rm $(FRONTEND_IMAGE)-container > /dev/null 2>&1 || true \
		&& echo " => $(FRONTEND_IMAGE)-container stopped and removed: ✅"
	
	@echo "🛑 STOPPING $(BACKEND_IMAGE)-container"
	@docker stop $(BACKEND_IMAGE)-container > /dev/null 2>&1 || true \
		&& docker rm $(BACKEND_IMAGE)-container > /dev/null 2>&1 || true \
		&& echo " => $(BACKEND_IMAGE)-container stopped and removed: ✅"


clean:
	@echo "🗑️ REMOVING IMAGE $(FRONTEND_IMAGE) and AP_DEPLOY_DIR $(FRONTEND_DEPLOY_DIR)"
	@echo "🛑 Stopping and removing containers using $(FRONTEND_IMAGE)"
	@docker rm -f $$(docker ps -aq --filter ancestor=$(FRONTEND_IMAGE)) 2>/dev/null || true
	@if docker image inspect $(FRONTEND_IMAGE) >/dev/null 2>&1; then \
		docker rmi -f $(FRONTEND_IMAGE) && echo " => Removed image $(FRONTEND_IMAGE) : ✅"; \
	else \
		echo " => Image $(FRONTEND_IMAGE) not found, skipping removal"; \
	fi
	@rm -rf $(FRONTEND_DEPLOY_DIR) \
		&& echo " => Removed dir $(FRONTEND_DEPLOY_DIR): ✅"

	@echo "🗑️ REMOVING IMAGE $(BACKEND_IMAGE) and BACKEND_DEPLOY_DIR $(BACKEND_DEPLOY_DIR)"
	@echo "🛑 Stopping and removing containers using $(BACKEND_IMAGE)"
	@docker rm -f $$(docker ps -aq --filter ancestor=$(BACKEND_IMAGE)) 2>/dev/null || true
	@if docker image inspect $(BACKEND_IMAGE) >/dev/null 2>&1; then \
		docker rmi -f $(BACKEND_IMAGE) && echo " => Removed image $(BACKEND_IMAGE): ✅"; \
	else \
		echo " => Image $(BACKEND_IMAGE) not found, skipping removal"; \
	fi
	@rm -rf $(BACKEND_DEPLOY_DIR) \
		&& echo " => Removed dir $(BACKEND_DEPLOY_DIR): ✅"

	@echo "🗑️ REMOVING IMAGE $(MLFLOW_IMAGE) and MLFLOW_DEPLOY_DIR $(MLFLOW_DEPLOY_DIR)"
	@echo "🛑 Stopping and removing containers using $(MLFLOW_IMAGE)"
	@docker rm -f $$(docker ps -aq --filter ancestor=$(MLFLOW_IMAGE)) 2>/dev/null || true
	@if docker image inspect $(MLFLOW_IMAGE) >/dev/null 2>&1; then \
		docker rmi -f $(MLFLOW_IMAGE) && echo " => Removed image $(MLFLOW_IMAGE): ✅"; \
	else \
		echo " => Image $(MLFLOW_IMAGE) not found, skipping removal"; \
	fi
	@docker image prune -f \
		&& echo " => Removed dangling images: ✅"
	@rm -rf $(MLFLOW_DEPLOY_DIR) \
		&& echo " => Removed dir $(MLFLOW_DEPLOY_DIR): ✅"


# SET Variables for Interactive mode option
DOCKER_IT := $(if $(filter y, $(I)), -it,)
MSG_IT := $(if $(filter y, $(I)), [INTERACTIVE MODE],)
SHELL_FRONTEND_MSG := $(if $(filter y,$(I)), => 💻 Access $(FRONTEND_IMAGE)-container shell with make shell CONTAINER=fe)
SHELL_BACKEND_MSG := $(if $(filter y,$(I)), => 💻 Access $(BACKEND_IMAGE)-container shell with make shell CONTAINER=be)

run:
ifeq ($(IMG), fe)  
	@echo "🐳 Creating and running $(FRONTEND_IMAGE)-container from $(FRONTEND_IMAGE) $(MSG_IT)"
	@docker rm -f $(FRONTEND_IMAGE)-container 2>/dev/null || true
	@echo "$(SHELL_FRONTEND_MSG)"
	@docker run \
		--env-file .env \
		--rm \
		$(DOCKER_IT) \
		-p $(PORT_REV_PROXY_FRONTEND_EXTERNAL):$(PORT_REV_PROXY_FRONTEND_EXPOSED) \
		--name $(FRONTEND_IMAGE)-container $(FRONTEND_IMAGE);
	@echo "🛑 STOPPING $(FRONTEND_IMAGE)-container"
else ifeq ($(IMG), be)
# Start MLflow (always remove previous container if exists)
# THIS MLFLOW SERVER IS NOT USED BY BACKEND SERVER IN LOCAL DEPLOY MODE
# SINCE NGINX.CONF/LOCATION/MLFLOW PROXY_PASS FORWARDS TO ANOTHER URL (=THIS SERVER DEPLOYED ONLINE)
# SEE MLFLOW_PROXY_PASS IN .ENV
# LEFT FOR PRE DEPLOY REASONS
# HAS TO BE DEPLOYED ONCE FULLY OPERATIONAL
	@echo "🐳 Starting MLflow container..."
	@echo " => Fake container run - Use the deployed version on HF Spaces"
	@echo " => MLFlow link in backend home page forwards to deployed version $(MLFLOW_PROXY_PASS)"
# Start Backend	
	@echo "🐳 Creating and running $(BACKEND_IMAGE)-container from $(BACKEND_IMAGE) $(MSG_IT)"
	@docker rm -f $(BACKEND_IMAGE)-container 2>/dev/null || true
	@echo "$(SHELL_BACKEND_MSG)"
	@docker run \
		--env-file .env \
		--rm \
		$(DOCKER_IT) \
		-p $(PORT_REV_PROXY_BACKEND_EXTERNAL):$(PORT_REV_PROXY_BACKEND_EXPOSED) \
		--name $(BACKEND_IMAGE)-container $(BACKEND_IMAGE);
	@echo "🛑 STOPPING $(BACKEND_IMAGE)-container"
else
	@echo "❌ Error : IMG not recognized. Use IMG=fe ou IMG=be"
endif

shell:
# Open shell in container
# fe: front end
# be: back end
# Must have run-interactive
ifeq ($(CONTAINER), fe)  
	@echo "🐳 Opening $(FRONTEND_IMAGE)-container bash"
	@docker exec -it $(FRONTEND_IMAGE)-container bash
else ifeq ($(CONTAINER), be)
	@echo "🐳 Opening $(BACKEND_IMAGE)-container bash"
	@docker exec -it $(BACKEND_IMAGE)-container bash
else
	@echo "❌ Error : CONTAINER not recognized. Use CONTAINER=fe ou CONTAINER=be"
endif

##########################################################################################################################
##########                    HF DEPLOY                                                                         ##########
##########################################################################################################################
# SERVER_DIR definition
ifeq ($(SERVER), be)
  SERVER_DIR := $(HF_BE_SERVER)
endif
ifeq ($(SERVER), fe)
  SERVER_DIR := $(HF_FE_SERVER)
endif
ifeq ($(SERVER), mf)
  SERVER_DIR := $(HF_MLFLOW_SERVER)
endif

push:
# Copy local servers deploy dirs in HFSPACES_DEPLOY_DIR, a temporary dir, before pushing to Hugging Face
# Modify listen directive in nginx/default.conf to enable HF to listen to its default port 7860 for each server
# For local pre deploy, these ports are set to PORT_REV_PROXY_FRONTEND_EXPOSED and PORT_REV_PROXY_BACKEND_EXPOSED
# They need to be different locally because 2 instances of nginx run on the same machine
# HF deployment uses 3 env variables whose values must correspond to HF blank docker spaces names
	@echo "🤗 Push to HF SPACES"
	@if [ ! -d "$(HFSPACES_DEPLOY_DIR)" ]; then \
		mkdir -p $(HFSPACES_DEPLOY_DIR) && \
		echo "Dir created automatically by make push" > $(HFSPACES_DEPLOY_DIR)/README.txt && \
		echo " => Created $(HFSPACES_DEPLOY_DIR): ✅"; \
	fi
	@if [ -z "$(SERVER)" ]; then \
		echo "❌ Error: USE: make push SERVER=be|fe|mf MSG=\"...\""; \
		exit 1; \
	fi
	@if [ -z "$(MSG)" ]; then \
		echo "❌ Error: missing commit message (USE: make push SERVER=be|fe|mf MSG=\"...\")"; \
		exit 1; \
	fi
	@if [ "$(SERVER)" = "be" ]; then \
		echo "⚙️  Pushing Backend server to HF" && \
		if [ ! -d "$(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)" ]; then \
			echo "⬇️  Cloning Hugging Face repo for backend..." && \
			git -C $(HFSPACES_DEPLOY_DIR) clone https://huggingface.co/spaces/$(HF_ACCOUNT)/$(SERVER_DIR) && \
			echo " => Repo cloned: ✅"; \
		else \
			echo "⚠️  Repo clone already exists in $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR), skipping git clone"; \
		fi && \
		cp -r $(BACKEND_DEPLOY_DIR)/* $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/ && \
		echo " => Copied predeployment $(BACKEND_DEPLOY_DIR) to $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/: ✅" && \
		sed -i "/server {/,/}/ s/\(listen \)$$PORT_REV_PROXY_BACKEND_EXPOSED/\1$$PORT_REV_PROXY_FRONTEND_EXPOSED/" $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/$(REV_PROXY_DIR_DEST)/default.conf && \
		echo " => Modified $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/$(REV_PROXY_DIR_DEST)/default.conf: ✅"; \
	elif [ "$(SERVER)" = "fe" ]; then \
		echo "⚙️  Pushing Frontend server to HF" && \
		if [ ! -d "$(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)" ]; then \
			echo "⬇️  Cloning Hugging Face repo for frontend..." && \
			git -C $(HFSPACES_DEPLOY_DIR) clone https://huggingface.co/spaces/$(HF_ACCOUNT)/$(SERVER_DIR) && \
			echo " => Repo cloned: ✅"; \
		else \
			echo "⚠️  Repo clone already exists in $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR), skipping git clone"; \
		fi && \
		cp -r $(FRONTEND_DEPLOY_DIR)/* $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/ && \
		echo " => Copied predeployment $(FRONTEND_DEPLOY_DIR) to $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/: ✅"; \
	elif [ "$(SERVER)" = "mf" ]; then \
		echo "⚙️  Pushing MLFLow server HF" && \
		if [ ! -d "$(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)" ]; then \
			echo "⬇️  Cloning Hugging Face repo for mlflow..." && \
			git -C $(HFSPACES_DEPLOY_DIR) clone https://huggingface.co/spaces/$(HF_ACCOUNT)/$(SERVER_DIR) && \
			echo " => Repo cloned: ✅"; \
		else \
			echo "⚠️  Repo clone already exists in $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR), skipping git clone"; \
		fi && \
		cp -r $(MLFLOW_DEPLOY_DIR)/* $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/ && \
		echo " => Copied predeployment $(MLFLOW_DEPLOY_DIR) to $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR)/: ✅"; \
	else \
		echo "❌ Unknown target: $(SERVER)"; \
		exit 1; \
	fi
	@git -C $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR) add . && \
		git -C $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR) commit -m "$(MSG)" || true && \
		git -C $(HFSPACES_DEPLOY_DIR)/$(SERVER_DIR) push

##########################################################################################################################
##########                    HELP SECTION                                                                      ##########
##########################################################################################################################
help:
	@echo ""
	@echo "🚀 Makefile Commands"
	@echo "============================================================================================="
	@echo ""
	@echo " 🏠 LOCAL DEVELOPMENT"
	@echo "    compose"
	@echo "         🧩 Build and run all services with Docker Compose"
	@echo "            Services: FastAPI + FastAPI-backend + Streamlit + MLflow + Nginx"
	@echo ""
	@echo " 🏗️  BUILD & LOCAL DEPLOYMENT"
	@echo "    build"
	@echo "         📦 Build Docker images for deployment"
	@echo "            Images: $(FRONTEND_IMAGE) $(BACKEND_IMAGE) $(MLFLOW_IMAGE)"
	@echo ""
	@echo "    run IMG=<target> I=<mode>"
	@echo "         🐳 Run deployment container"
	@echo "            Options: IMG=fe|be	→ Front End/Back End"
	@echo "                     I=y|n	→ Interactive mode"
	@echo ""
	@echo "    shell CONTAINER=<target>"
	@echo "         🐚  Open bash shell in running container"
	@echo "             Option: CONTAINER=fe|be"
	@echo ""
	@echo "    stop"
	@echo "         🛑 Stop and remove all deployment containers"
	@echo ""
	@echo "    clean"
	@echo "         🗑️  Remove deployment images and directories"
	@echo ""
	@echo " 🤗 HUGGING FACE SPACES DEPLOYMENT"
	@echo "    push SERVER=<target> MSG=<commit_message>"
	@echo "         ⚙️  Create deployment container, (clone), and push to HF Spaces"
	@echo "            Options: SERVER=fe|be|mf	→ Front End//Back End/MLFlow"
	@echo "                     MSG=...		→ Commit message"
	@echo ""
	@echo " ❓  Need help? Check README.md or run specific commands to see detailed output"
	@echo ""