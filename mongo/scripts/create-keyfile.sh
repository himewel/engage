#!/usr/bin/env bash

echo "Checking if keyfile already exists..."

if [ ! -e "/mongo-storage/keyfile" ]; then
    echo "Creating keyfile in /mongo-storage..."
    openssl rand -base64 741 >> /mongo-storage/keyfile
    chmod 0400 /mongo-storage/keyfile
    chown mongodb /mongo-storage/keyfile
else
    echo "Keyfile already exists"
fi

ls -l /mongo-storage
