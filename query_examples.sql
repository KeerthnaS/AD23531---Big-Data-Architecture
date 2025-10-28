-- Top anomalous readings (highest anomaly_score)
SELECT meter_id, timestamp, kwh, anomaly_score
FROM `<PROJECT_ID>.energy_theft.features`
ORDER BY anomaly_score DESC
LIMIT 20;

-- Daily aggregation with anomaly counts
WITH daily AS (
  SELECT meter_id, DATE(timestamp) AS dt, SUM(kwh) AS daily_kwh, AVG(anomaly_score) as avg_anomaly
  FROM `<PROJECT_ID>.energy_theft.features`
  GROUP BY meter_id, dt
)
SELECT dt, COUNTIF(avg_anomaly > 1.0) AS suspicious_meters
FROM daily
GROUP BY dt
ORDER BY dt DESC
LIMIT 30;

-- Top meters with sustained anomalies
SELECT meter_id, AVG(anomaly_score) AS mean_score, COUNT(*) AS samples
FROM `<PROJECT_ID>.energy_theft.features`
GROUP BY meter_id
HAVING AVG(anomaly_score) > 0.8
ORDER BY mean_score DESC
LIMIT 50;
