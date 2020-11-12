#!/bin/sh

centre="apa_arq_lop_ote"

cd /usr/src/spark/

echo "[Sensor] - Init server socket"
python3 sensor/socket_server.py "$1" "$2" $centre &

sleep 5

echo "[Occupation] - Init server socket"
port_occupation=$(expr "$2" - 1)
python3  occupation/socket_server.py "$1" "$port_occupation" $centre &

sleep 5

echo "[Sensor] - Process extract data"
spark-submit --total-executor-cores 2  sensor/extract_spark.py "$1" "$2" &

sleep 5

echo "[Occupation] - Process extract data"
spark-submit --total-executor-cores 2  occupation/extract_spark.py "$1" "$port_occupation" &

sleep 5

while true
do
    echo "Transform and load in final file"
    sleep 20
    spark-submit --total-executor-cores 2 transform_spark.py
done