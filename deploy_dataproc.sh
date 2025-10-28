#!/usr/bin/env bash
# Usage: bash deploy_dataproc.sh <PROJECT_ID> <REGION> <CLUSTER_NAME>
PROJECT_ID=${1:-$PROJECT_ID}
REGION=${2:-us-central1}
CLUSTER=${3:-theft-cluster}

if [ -z "$PROJECT_ID" ]; then
  echo "Please provide PROJECT_ID as first argument or set the PROJECT_ID env var."
  exit 1
fi

gcloud config set project $PROJECT_ID
gcloud services enable dataproc.googleapis.com

echo "Creating Dataproc cluster: $CLUSTER in $REGION for project $PROJECT_ID ..."
gcloud dataproc clusters create $CLUSTER \
  --region=$REGION \
  --single-node \
  --image-version=2.1-debian11 \
  --optional-components=JUPYTER \
  --enable-component-gateway
