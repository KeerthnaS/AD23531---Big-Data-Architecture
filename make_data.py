#!/usr/bin/env python3
"""Generate synthetic smart-meter data and optionally upload to a GCS bucket.

Usage:
  python3 make_data.py                # writes meter_readings.csv locally
  python3 make_data.py --upload gs://my-bucket/raw/   # also uploads to GCS (requires gsutil & authenticated gcloud)

Notes:
- Designed to run in Cloud Shell (gcloud authenticated) or locally.
- If pandas is not installed, it will attempt to install it for the user (requires network).
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime
import random

# Try to import pandas & numpy, install if missing
try:
    import pandas as pd, numpy as np
except Exception as e:
    print("pandas or numpy not available; attempting to install via pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pandas", "numpy"])
    import pandas as pd, numpy as np

def generate_csv(n_meters=50, start='2025-01-01', end='2025-01-15', freq='H', out='meter_readings.csv', theft_prob=0.01):
    hours = pd.date_range(start, end, freq=freq)
    data = []
    for m in range(n_meters):
        base = np.random.uniform(0.5, 2.5)  # average kWh per hour for this meter
        for t in hours:
            kwh = base + np.random.normal(0, 0.2)
            if np.random.rand() < theft_prob:
                # inject theft-like drop (randomly)
                kwh *= np.random.uniform(0.1, 0.4)
            data.append([int(m), t.strftime('%Y-%m-%d %H:%M:%S'), float(round(kwh, 3))])
    df = pd.DataFrame(data, columns=['meter_id', 'timestamp', 'kwh'])
    df.to_csv(out, index=False)
    print(f"Created {out} with {len(df)} rows")
    return out

def upload_to_gcs(local_file, gcs_path):
    # gcs_path should be like gs://bucket/path/
    print(f"Uploading {local_file} to {gcs_path} ...")
    cmd = ["gsutil", "cp", local_file, gcs_path]
    subprocess.check_call(cmd)
    print("Upload complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', help='GCS destination prefix (e.g. gs://my-bucket/raw/)', default=None)
    parser.add_argument('--meters', type=int, default=50)
    parser.add_argument('--out', default='meter_readings.csv')
    args = parser.parse_args()

    csv_file = generate_csv(n_meters=args.meters, out=args.out)
    if args.upload:
        upload_to_gcs(csv_file, args.upload)
