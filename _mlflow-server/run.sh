#!/bin/bash
source ../.env 2>/dev/null || true
set -e

# Map boto AWS Creds var by ENV
export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY"
export AWS_DEFAULT_REGION="$AWS_REGION"

echo "--------------------------------------------"
echo "Starting MLflow server"
echo "Listening port = ${PORT_MLFLOW_TRACKING_EXTERNAL}"
echo "BACKEND_STORE_URI = ${BACKEND_STORE_URI:0:10}"
echo "ARTIFACT_ROOT = ${ARTIFACT_ROOT:0:8}"
echo "AWS_ACCESS_KEY_ID = ${AWS_ACCESS_KEY_ID:0:2}***" # Debug 
echo "AWS_SECRET_ACCESS_KEY = ${AWS_SECRET_ACCESS_KEY:0:2}***" # Debug 
echo "AWS_DEFAULT_REGION = ${AWS_DEFAULT_REGION:0:2}***" # Debug 
echo "--------------------------------------------"

# S3 Connectivity test
echo "Testing S3 connectivity... Check AWS Creds "
python3 -c "
import boto3
try:
    s3 = boto3.client('s3')
    bucket = '$ARTIFACT_ROOT'.split('/')[2]
    s3.head_bucket(Bucket=bucket)
    print('✅ S3 access OK')
except Exception as e:
    print(f'❌ S3 access failed: {e}')
"

# cf. seccurity options/mlflow -> https://mlflow.org/docs/latest/self-hosting/security/network/
# Start MLflow
exec mlflow server \
    --host 0.0.0.0 \
    --port "$PORT_MLFLOW_TRACKING_EXTERNAL" \
    --backend-store-uri "$BACKEND_STORE_URI" \
    --default-artifact-root "$ARTIFACT_ROOT" \
    --disable-security-middleware