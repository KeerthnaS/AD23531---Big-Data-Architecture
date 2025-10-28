# Energy Theft Anomaly Detection — GCP + Dataproc + BigQuery Demo

This repository contains a small end-to-end demo for **Energy Theft and Anomaly Detection** using **Google Cloud Platform (GCP)** and **Dataproc (PySpark)**.
It includes synthetic data generation, feature engineering on Dataproc, loading results into BigQuery, and instructions for visualization in Looker Studio.

> **Important:** Replace placeholder values like `<PROJECT_ID>` and `<BUCKET_NAME>` with your actual GCP project ID and Cloud Storage bucket name before running the scripts.

---

## Repository structure

```
/ (root)
├─ README.md                     - this file
├─ make_data.py                  - generate synthetic meter data (CSV) and upload to GCS
├─ feature_engineering.py        - PySpark job to compute rolling features and anomaly_score
├─ deploy_dataproc.sh            - commands to create a Dataproc cluster (example)
├─ submit_job.sh                 - command to submit the pyspark job to the cluster
├─ load_bigquery.sh              - bq commands to create dataset and load processed parquet
├─ query_examples.sql            - sample BigQuery queries to explore anomalies
├─ looker_instructions.md        - short instructions for connecting BigQuery to Looker Studio
├─ requirements.txt              - Python packages used for local testing
├─ .gitignore
└─ LICENSE
```

---

## Quick steps (copy-paste)

1. Set your project and variables (in Cloud Shell):
```bash
export PROJECT_ID=<PROJECT_ID>
export BUCKET_NAME=<BUCKET_NAME>   # e.g. energy-theft-demo-01
gcloud config set project $PROJECT_ID
```

2. Create the GCS bucket (if not already created):
```bash
gsutil mb -l us-central1 gs://$BUCKET_NAME/
```

3. Generate synthetic data locally (Cloud Shell) and upload to GCS:
```bash
python3 make_data.py --upload gs://$BUCKET_NAME/raw/
```

4. Create Dataproc cluster (example):
```bash
bash deploy_dataproc.sh $PROJECT_ID us-central1 theft-cluster
```

5. Submit the PySpark job:
```bash
bash submit_job.sh theft-cluster us-central1 feature_engineering.py
```

6. Load processed Parquet into BigQuery:
```bash
bash load_bigquery.sh $PROJECT_ID $BUCKET_NAME
```

7. Query the results (example):
```bash
bq query --use_legacy_sql=false 'SELECT meter_id, timestamp, kwh, anomaly_score FROM `'$PROJECT_ID'.energy_theft.features` ORDER BY anomaly_score DESC LIMIT 20'
```

See files and comments below for more details and customization.

---
