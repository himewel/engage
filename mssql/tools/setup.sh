#!/usr/bin/env bash

hostname=$MSSQL_HOST
port=$MSSQL_PORT
username=$MSSQL_USER
password=$MSSQL_PASSWD

echo "Waiting MSSQL to be up on ${hostname}:${port}..."
while ! nc -z ${hostname} ${port}; do
    sleep 10
done

echo "Checking if data its already there..."
response=$(/opt/mssql-tools/bin/sqlcmd \
    -S ${hostname} \
    -U ${username} \
    -P ${password} \
    -h -1 \
    -i /home/mssql/sql/check_schema.sql)

echo "Extracting data from api..."
python3 /home/mssql/tools/setup.py

echo "Creating tables..."
/opt/mssql-tools/bin/sqlcmd \
    -S ${hostname} \
    -U ${username} \
    -P ${password} \
    -h -1 \
    -e \
    -i /home/mssql/sql/create_tables.sql

echo "Ingesting data into mssql tables..."
ls $CSV_PATH
for file in ${SQL_PATH}/*.sql; do
    echo "Running ${file}..."
    /opt/mssql-tools/bin/sqlcmd \
        -S ${hostname} \
        -U ${username} \
        -P ${password} \
        -e \
        -i ${file}
done
