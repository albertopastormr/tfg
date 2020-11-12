from pyspark.sql import SparkSession
import sys, os, time
from pyspark.sql.types import *

if len(sys.argv) < 3:
    print("WARN: Es necesario poner dos agumentos: <IP> <Port>")
    sys.exit(0)

print("-------Limpieza buffer--------")
os.system('rm -rf /usr/src/spark/data_sensor /usr/src/spark//checkpoint_sensor')
print("------------------------------")

spark = SparkSession \
    .builder \
    .appName("SensorProcess") \
    .getOrCreate()

os.system('bash /usr/src/spark/sensor/unificate_files.sh &')

spark.sparkContext.setLogLevel('WARN')

# Create DataFrame representing the stream of input lines from connection to localhost:9999
df_socket = spark \
    .readStream \
    .format("socket") \
    .option("host", str(sys.argv[1])) \
    .option("port", int(sys.argv[2])) \
    .load()

query = df_socket\
    .writeStream\
    .queryName("extract_data_sensor")\
    .format("csv")\
    .option("path", "/usr/src/spark/data_sensor")\
    .option("checkpointLocation", "/usr/src/spark/checkpoint_sensor")\
    .start()

query.awaitTermination()

print("-------Limpieza buffer--------")
os.system('rm -rf /usr/src/spark/data_sensor /usr/src/spark//checkpoint_sensor')
print("------------------------------")
