#!/usr/bin/env bash
# Usage: bash submit_job.sh <CLUSTER_NAME> <REGION> <PYSPARK_FILE>
CLUSTER=${1:-theft-cluster}
REGION=${2:-us-central1}
PYFILE=${3:-feature_engineering.py}

echo "Submitting PySpark job $PYFILE to cluster $CLUSTER in region $REGION..."
gcloud dataproc jobs submit pyspark $PYFILE --cluster=$CLUSTER --region=$REGION
echo "Job submitted."
