#!/bin/sh

rm -rf final.csv

while true; do
  sleep 5
  echo "---"
  echo "Union all files .csv to final.csv..."
  cat data/part-*.csv > stream-data.csv
  sed 's/"//g' stream-data.csv > data/stream-data-aux.csv
  sed '/^$/d' data/stream-data-aux.csv > stream-data.csv
  cat stream-data.csv | sort -n --field-separator=',' --key=1 > stream-data-final.csv
  echo "Unificate and cleaned."
  echo "---"
done
