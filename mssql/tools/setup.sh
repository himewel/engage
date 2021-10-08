#!/usr/bin/env bash

set -e

echo "Waiting MSSQL to be up on localhost:1433..."
while ! nc -z localhost 1433; do
    sleep 10
done

sleep 5

echo "Creating tables..."
/opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U sa \
    -P ${SA_PASSWORD} \
    -h -1 \
    -e \
    -i /home/mssql/tools/create_tables.sql

echo "Ingesting data from api..."
python3 /home/mssql/tools/setup.py
