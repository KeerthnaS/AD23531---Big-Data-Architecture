# PySpark job for Dataproc: compute rolling features and anomaly score, write Parquet to GCS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, stddev, abs as spark_abs
from pyspark.sql.window import Window

def main():
    spark = SparkSession.builder.appName("FeatureEngineering").getOrCreate()

    # REPLACE the path if your bucket name differs
    INPUT_PATH = "gs://<BUCKET_NAME>/raw/meter_readings.csv"
    OUTPUT_PATH = "gs://<BUCKET_NAME>/processed/features/"

    df = spark.read.csv(INPUT_PATH, header=True, inferSchema=True)
    df = df.withColumn('timestamp', col('timestamp').cast('timestamp'))

    # rolling window of past 24 hours (including current)
    windowSpec = Window.partitionBy('meter_id').orderBy('timestamp').rowsBetween(-24, 0)
    df = df.withColumn('rolling_mean', avg('kwh').over(windowSpec))
    df = df.withColumn('rolling_std', stddev('kwh').over(windowSpec))
    df = df.fillna(0)

    # anomaly score using scaled deviation
    df = df.withColumn('anomaly_score', spark_abs(col('kwh') - col('rolling_mean')) / (col('rolling_std') + 1e-3))

    # write outputs as Parquet for BigQuery efficient load
    df.write.mode('overwrite').parquet(OUTPUT_PATH)
    print('✅ Saved processed data to GCS ->', OUTPUT_PATH)

if __name__ == '__main__':
    main()
