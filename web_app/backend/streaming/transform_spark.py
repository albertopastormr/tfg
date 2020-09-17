from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.window import Window
from pyspark.sql.functions import *
import random
import os

sc = SparkContext()
sqlContext = SQLContext(sc)

file_origin_occupation = "/tmp/datasets/occupation/simulation_occupation.csv"
file_origin_sensor = "/tmp/datasets/sensor/simulation_sensor.csv"

spark = SparkSession \
    .builder \
    .appName("Transform_final_csv") \
    .getOrCreate()

df_occupation = spark.read.load(file_origin_occupation, format="csv", sep=",", inferSchema="true", header="true")
df_sensor = spark.read.load(file_origin_sensor, format="csv", sep=",", inferSchema="true", header="true")

#df_occupation.show()
#df_sensor.show()

df_occupation = df_occupation.withColumnRenamed("-1", "index")
df_sensor = df_sensor.withColumnRenamed("-1", "index")

df_sensor = df_sensor.withColumn("today_consume", sum(col("consumo")).over(Window.partitionBy("centro").orderBy("index")))
df_occupation = df_occupation.withColumn("today_occupation", sum(col("num_occupation")).over(Window.partitionBy("centre").orderBy("index")))

# registramos como tablas temporales
df_occupation.registerTempTable("occupation")
df_sensor.registerTempTable("consume")

# Hacemos join por el id y nos quedamos con las columnas que nos interesa
df_total = sqlContext.sql("select "
               "    ocu.index, "
               "    ocu.centre, "
               "    ocu.time_extract, "
               "    con.consumo as consume, "
               "    con.coste as cost, "
               "    ocu.num_occupation, "
               "    ocu.num_students, "
               "    ocu.num_staff, "
               "    con.today_consume, "
               "    ocu.today_occupation "
               "from occupation ocu "
               "join consume con "
               "on ocu.index = con.index ")


def positive_or_negative():
    if random.random() < 0.5:
        return 1
    else:
        return -1

df_total = df_total.withColumn("today_person", (col("consume") / col("num_occupation")))
df_total = df_total.withColumn("yesteday_consume", (col("consume") + positive_or_negative()))
df_total = df_total.withColumn("yesterday_occupation", (col("num_occupation") + positive_or_negative()))
df_total = df_total.withColumn("yesterday_person", (col("today_person") + (random.random() * 2 - 1)))

df_total.show()

df_total.coalesce(1).write.format('csv').option('header',True).mode('overwrite').option('sep',',').save('/tmp/datasets/real_time')

os.system("cat /tmp/datasets/real_time/part-*.csv > /tmp/datasets/real_time.csv")

#-1,centre,time_extract,consume,cost,num_occupation,num_students,num_staff,today_consume,today_occupation,today_person, yesteday_consume,yesterday_occupation,yesterday_person
#0,AP ARQ. LOPEZ OTERO,2018-01-01 01:00,10,618.58,4,2,2,  10,4,"2,50",9,4,"2,50"
#1,AP ARQ. LOPEZ OTERO,2018-01-01 02:00,10,618.58,4,2,2,  20,8,"2,50",19,8,"2,50"

