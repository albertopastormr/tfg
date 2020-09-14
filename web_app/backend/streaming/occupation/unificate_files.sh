#!/bin/sh

#rm -rf /usr/src/spark/data_occupation/.part-*.csv.crc
#rm -rf /usr/src/spark/data_occupation/part-*.csv

while true; do
  sleep 10
  echo "---"
  echo "Union all files .csv to final.csv..."
  cat /usr/src/spark/data_occupation/part-*.csv > /usr/src/spark/data_occupation/stream-data.csv
  sed 's/"//g' /usr/src/spark/data_occupation/stream-data.csv > /usr/src/spark/data_occupation/stream-data-aux.csv
  sed '/^$/d' /usr/src/spark/data_occupation/stream-data-aux.csv > /usr/src/spark/data_occupation/stream-data.csv
  cat /usr/src/spark/data_occupation/stream-data.csv | sort -n --field-separator=',' --key=1 > /tmp/datasets/occupation/simulation_occupation.csv
  echo "Unificate and cleaned."
  echo "---"

done

