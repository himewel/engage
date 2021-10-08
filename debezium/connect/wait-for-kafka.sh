#!/usr/bin/env bash

set -e

echo "Waiting kafka to launch on ${BOOTSTRAP_SERVERS}..."
while ! nc -z ${BOOTSTRAP_SERVERS//\:/ }; do
    sleep 1
done

bash $@ &
/docker-entrypoint.sh start
