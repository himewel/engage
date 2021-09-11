FROM mcr.microsoft.com/mssql/server:2019-CU12-ubuntu-20.04

ENV PATH "${PATH}:/home/mssql/.local/bin"

USER root

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        netcat \
        python3-pip \
    && mkdir -p /home/mssql \
    && chown -R mssql /home/mssql

USER mssql

WORKDIR /home/mssql

COPY requirements.txt .

RUN pip3 install --no-cache-dir --requirement ./requirements.txt

COPY sql ./sql
COPY tools ./tools

CMD [ "bash", "/home/mssql/tools/setup.sh"]
