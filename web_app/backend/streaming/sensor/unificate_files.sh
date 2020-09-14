#!/bin/sh

#rm -rf /usr/src/spark/data_sensor/.part-*.csv.crc
#rm -rf /usr/src/spark/data_sensor/part-*.csv

while true; do
  sleep 10
  echo "---"
  echo "Union all files .csv to final.csv..."
  cat /usr/src/spark/data_sensor/part-*.csv > /usr/src/spark/data_sensor/stream-data.csv
  sed 's/"//g' /usr/src/spark/data_sensor/stream-data.csv > /usr/src/spark/data_sensor/stream-data-aux.csv
  sed '/^$/d' /usr/src/spark/data_sensor/stream-data-aux.csv > /usr/src/spark/data_sensor/stream-data.csv
  cat /usr/src/spark/data_sensor/stream-data.csv | sort -n --field-separator=',' --key=1 > /tmp/datasets/sensor/simulation_sensor.csv
  echo "Unificate and cleaned."
  echo "---"

  #python-submit transform_spark.py
done
