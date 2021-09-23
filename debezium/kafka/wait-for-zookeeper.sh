#!/usr/bin/env bash

echo "Waiting zookeeper server to launch on ${ZOOKEEPER_CONNECT}..."
while ! nc -z ${ZOOKEEPER_CONNECT//\:/ }; do
    sleep 1
done

bash /docker-entrypoint.sh start
