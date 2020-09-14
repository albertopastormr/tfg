from pyspark.sql import SparkSession

file_origin_occupation = "/tmp/datasets/occupation/simulation_occupation.csv"
file_origin_sensor = "/tmp/datasets/occupation/simulation_sensor.csv"

spark = SparkSession \
    .builder \
    .appName("Transform_final_csv") \
    .getOrCreate()

df_occupation = spark.read.load(file_origin_occupation, format="csv", sep=",", inferSchema="true", header="true")
df_sensor = spark.read.load(file_origin_sensor, format="csv", sep=",", inferSchema="true", header="true")





#-1,centre,time_extract,consume,cost,num_occupation,num_students,num_staff,today_consume,today_occupation,today_person,yesteday_consume,yesterday_occupation,yesterday_person
#0,AP ARQ. LOPEZ OTERO,2018-01-01 01:00,10,618.58,4,2,2,10,4,"2,50",9,4,"2,50"
#1,AP ARQ. LOPEZ OTERO,2018-01-01 02:00,10,618.58,4,2,2,20,8,"2,50",19,8,"2,50"

df_occupation.show()
df_sensor.show()