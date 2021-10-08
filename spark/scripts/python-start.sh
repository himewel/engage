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

python3 $SPARK_HOME/$@
