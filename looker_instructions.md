# Looker Studio (Data Studio) - Quick Connect Instructions

1. Open https://lookerstudio.google.com and log in with your Google account.
2. Click **Create → Data Source** → Select **BigQuery**.
3. Choose your project, dataset `energy_theft`, and table `features`.
4. Click **Connect** → **Add to Report**.
5. Recommended visuals:
   - Time series: X-axis `timestamp`, Metric `kwh` or `anomaly_score`.
   - Table: columns `meter_id`, `timestamp`, `kwh`, `anomaly_score` sorted by anomaly_score DESC.
   - Filters: Date range, Meter ID.
6. Use conditional formatting to highlight rows where `anomaly_score` > threshold (e.g. 0.8).
