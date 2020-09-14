#!/bin/sh

echo "[Sensor] - Init server socket"
python3 sensor/socket_server.py "$1" "$2" "$3" &

sleep 5

echo "[Occupation] - Init server socket"
port_occupation=$(expr "$2" - 1)
python3  occupation/socket_server.py "$1" "$port_occupation" "$3" &

sleep 5

echo "[Sensor] - Process extract data"
spark-submit  sensor/extract_spark.py "$1" "$2" &

sleep 5

echo "[Occupation] - Process extract data"
spark-submit  occupation/extract_spark.py "$1" "$port_occupation" &

sleep 5

echo "[Sensor] - Transform and load in final file"
#python-submit transform_spark.py

