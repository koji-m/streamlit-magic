#!/bin/sh

PROJECT_ID=$1
SERVICE_NAME=$2
BUCKET_NAME=$3
BLOB_PATH=$4

GOOGLE_APPLICATION_CREDENTIALS='/app/key.json'
SERVICE_ACCOUNT_EMAIL=$(cat $GOOGLE_APPLICATION_CREDENTIALS | jq -r .client_email)

gcloud auth activate-service-account \
  ${SERVICE_ACCOUNT_EMAIL} \
  --key-file ${GOOGLE_APPLICATION_CREDENTIALS} \
  --project ${PROJECT_ID}

gsutil -m cp gs://${BUCKET_NAME}/${BLOB_PATH} /app/

streamlit run /app/${SERVICE_NAME}.py --server.port $PORT

