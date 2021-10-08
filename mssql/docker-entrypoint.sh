#!/usr/bin/env bash

set -e

bash /home/mssql/tools/setup.sh &
/opt/mssql/bin/sqlservr
