#!/usr/bin/env bash

SCRIPT=$1

echo "Waiting kafka broker to launch on ${BROKER_HOSTNAME}..."
while ! nc -z ${BROKER_HOSTNAME//\:/ }; do
    sleep 1
done

spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master local \
    --packages \
        org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    $SCRIPT
