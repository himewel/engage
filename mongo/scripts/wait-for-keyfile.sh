#!/usr/bin/env bash

echo "Waiting for a keyfile in /mongo-storage/keyfile..."
while [ ! -e "/mongo-storage/keyfile" ]; do
    sleep 1
done
