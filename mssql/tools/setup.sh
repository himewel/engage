#!/usr/bin/env bash

hostname=$MSSQL_HOST
port=$MSSQL_PORT
username=$MSSQL_USER
password=$MSSQL_PASSWD

echo "Waiting MSSQL to be up on ${hostname}:${port}..."
while ! nc -z ${hostname} ${port}; do
    sleep 10
done

sleep 5

echo "Creating tables..."
/opt/mssql-tools/bin/sqlcmd \
    -S ${hostname} \
    -U ${username} \
    -P ${password} \
    -h -1 \
    -e \
    -i /home/mssql/tools/create_tables.sql

echo "Ingesting data from api..."
python3 /home/mssql/tools/setup.py
