#!/usr/bin/env bash

cd ./scripts
bash ./create-keyfile.sh

echo "Waiting for primary node..."
until curl http://mongodb:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
    sleep 1
done

echo "Waiting for secondary node..."
until curl http://mongodb-rs:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
    sleep 1
done

echo "Starting replicas..."
mongosh --host mongodb:27017 -u root -p root ./start-replica.js
