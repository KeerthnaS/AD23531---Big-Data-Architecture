#!/usr/bin/env bash
# Usage: bash load_bigquery.sh <PROJECT_ID> <BUCKET_NAME>
PROJECT=${1:-$PROJECT_ID}
BUCKET=${2:-<BUCKET_NAME>}

if [ -z "$PROJECT" ] || [ -z "$BUCKET" ]; then
  echo "Usage: bash load_bigquery.sh <PROJECT_ID> <BUCKET_NAME>"
  exit 1
fi

gcloud config set project $PROJECT

# Create dataset
bq --location=US mk -d ${PROJECT}:energy_theft || true

# Load Parquet files into BigQuery table 'features'
bq load --autodetect --source_format=PARQUET   energy_theft.features gs://$BUCKET/processed/features/*.parquet
echo "BigQuery load complete. Table: ${PROJECT}:energy_theft.features"
