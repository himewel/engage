#!/usr/bin/env bash

SCRIPT=$@

echo "Waiting kafka broker to launch on ${BROKER_HOSTNAME}..."
while ! nc -z ${BROKER_HOSTNAME//\:/ }; do
    sleep 1
done

echo "Waiting hadoop to launch on ${HADOOP_HOSTNAME}..."
while ! nc -z ${HADOOP_HOSTNAME//\:/ }; do
    sleep 1
done

spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.ui.port=$SPARK_UI_PORT \
    --master local \
    --packages \
        org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    $SCRIPT
