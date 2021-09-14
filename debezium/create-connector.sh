#!/usr/bin/env bash

echo "Waiting 60 seconds before startup..."
sleep 60

echo "Waiting DBZ_SOURCE to launch on ${DBZ_SOURCE}..."
while ! nc -z ${DBZ_SOURCE//\:/ }; do
    sleep 1
done

echo "Waiting DBZ_CONNECT to launch on ${DBZ_CONNECT}..."
while ! nc -z ${DBZ_CONNECT//\:/ }; do
    sleep 1
done

for file in ./connectors/*.json; do
    curl --include \
        --request POST \
        --header "Accept:application/json" \
        --header "Content-Type:application/json" \
        --data @${file} \
        ${DBZ_CONNECT}/connectors/
done
