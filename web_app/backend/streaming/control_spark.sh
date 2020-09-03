#!/bin/sh

echo "Init socker spark"
python  ./../backend/streaming/socket_spark.py localhost 1234 &

sleep 5

echo "Init process spark"
spark-submit  ./../backend/streaming/prosecution_spark.py localhost 1234 &

sleep 5

