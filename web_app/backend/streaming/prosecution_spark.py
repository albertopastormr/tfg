from pyspark.sql import SparkSession
import sys, os

if len(sys.argv) < 3:
    print("WARN: Es necesario poner dos agumentos: <IP> <Port>")
    sys.exit(0)

print("-------Limpieza buffer--------")
os.system('rm -rf data checkpoint')
os.system('rm -rf *.csv')
print("------------------------------")

spark = SparkSession \
    .builder \
    .appName("SensorProcess") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", str(sys.argv[1])) \
    .option("port", int(sys.argv[2])) \
    .load()

#os.system('bash unificate_files.sh &')

query = lines\
    .writeStream\
    .queryName("extract_data_sensor")\
    .format("csv")\
    .option("path", "/usr/src/spark/data")\
    .option("checkpointLocation", "/usr/src/spark/checkpoint")\
    .start()


query.awaitTermination()

print("-------Limpieza buffer--------")
os.system('rm -rf data checkpoint')
os.system('rm -rf *.csv')
print("------------------------------")
