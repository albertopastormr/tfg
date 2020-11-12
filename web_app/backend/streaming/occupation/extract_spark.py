from pyspark.sql import SparkSession
import sys, os
from pyspark.sql.types import *

if len(sys.argv) < 3:
    print("WARN: Es necesario poner dos agumentos: <IP> <Port>")
    sys.exit(0)

print("-------Limpieza buffer--------")
os.system('rm -rf /usr/src/spark/data_occupation /usr/src/spark/checkpoint_occupation')
print("------------------------------")

spark = SparkSession \
    .builder \
    .appName("OccupationProcess") \
    .getOrCreate()

os.system('bash /usr/src/spark/occupation/unificate_files.sh &')

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
    .queryName("extract_data_occupation")\
    .format("csv")\
    .option("path", "/usr/src/spark/data_occupation")\
    .option("checkpointLocation", "/usr/src/spark/checkpoint_occupation")\
    .start()\
    .awaitTermination()

print("-------Limpieza buffer--------")
os.system('rm -rf /usr/src/spark/data_occupation /usr/src/spark/checkpoint_occupation')
print("------------------------------")
