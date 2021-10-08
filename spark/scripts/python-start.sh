#!/usr/bin/env bash

set -e

echo "Waiting kafka broker to launch on ${BROKER_HOSTNAME}..."
while ! nc -z ${BROKER_HOSTNAME//\:/ }; do
    sleep 1
done

python3 $SPARK_HOME/$@
