#!/usr/bin/env bash

set -e

if [ ! -e "/keyfile" ]; then
    echo "Creating keyfile in /mongo-storage..."
    openssl rand -base64 741 >> /keyfile
    chmod 0400 /keyfile
    chown mongodb /keyfile
else
    echo "Keyfile already exists"
fi

mongod \
    --bind_ip_all \
    --fork \
    --logpath /var/log/mongodb/mongod.log \
    --keyFile /keyfile \
    $@

cd ./scripts

echo "Waiting for primary node..."
until curl http://localhost:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
    sleep 1
done

sleep 20

echo "Starting replicas..."
mongo localhost:27017/engagedb ./start-replica.js
echo "Replica set initiated"

if [ ! -e "./admin_created" ]; then
    sleep 20

    echo "Creating admin user..."
    mongo localhost:27017/admin ./create-admin.js

    echo "Granting roles to debezium user..."
    mongo -u admin -p admin localhost:27017/admin ./grant-roles.js

    echo "Creating checkpoint file"
    touch ./admin_created
fi

tail +1f /var/log/mongodb/mongod.log
