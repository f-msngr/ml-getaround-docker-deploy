mlflow server conf dir
Dockerfile and run.sh will have their env variable $PORT_MLFLOW_TRACKING_EXTERNAL
automatically switched to $PORT_MLFLOW_HF_DEPLOYED_DEFAULT
and then this variable will be substituted by its value in .env
The changes are made by makefile in build/mlflow section