#!/usr/bin/env bash

mongod --bind_ip_all --fork --logpath /var/log/mongodb/mongod.log $@

cd ./scripts

echo "Waiting for primary node..."
until curl http://localhost:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
    sleep 1
done

sleep 20

echo "Starting replicas..."
mongo localhost:27017/engagedb ./start-replica.js
echo "Initiated replica set"

sleep 10

echo "Creating admin user..."
mongo localhost:27017/admin ./create-admin.js

echo "Granting roles to debezium user..."
mongo -u admin -p admin localhost:27017/admin ./grant-roles.js

tail +1f /var/log/mongodb/mongod.log
