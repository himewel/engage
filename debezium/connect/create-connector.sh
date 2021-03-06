#!/usr/bin/env bash

set -e

echo "Waiting 30 seconds before startup..."
sleep 30

echo "Waiting DBZ_CONNECT to launch on ${HOSTNAME}:8083..."
while ! nc -z $HOSTNAME 8083; do
    sleep 1
done

for file in /connectors/*.json; do
    curl --include \
        --request POST \
        --header "Accept:application/json" \
        --header "Content-Type:application/json" \
        --data @${file} \
        ${HOSTNAME}:8083/connectors/
done
