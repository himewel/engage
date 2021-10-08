#!/usr/bin/env bash

set -e

echo "Waiting kafka broker to launch on ${BROKER_HOSTNAME}..."
while ! nc -z ${BROKER_HOSTNAME//\:/ }; do
    sleep 1
done

echo "Waiting hadoop to launch on ${HADOOP_HOSTNAME}..."
while ! nc -z ${HADOOP_HOSTNAME//\:/ }; do
    sleep 1
done

spark-submit \
    --conf spark.ui.port=$SPARK_UI_PORT \
    --num-executors $SPARK_NUM_EXECUTOR \
    --executor-cores $SPARK_EXECUTOR_CORES \
    --executor-memory $SPARK_EXECUTOR_MEMORY \
    --master local \
    --packages \
    org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    $@
