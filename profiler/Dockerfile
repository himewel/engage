FROM mcr.microsoft.com/mssql/server:2019-CU12-ubuntu-20.04

USER root

RUN apt-get update \
    && apt-get install --no-install-recommends --yes gnupg build-essential \
    && wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add - \
    && echo "deb [arch=amd64,arm64] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/5.0 multiverse" \
        | tee /etc/apt/sources.list.d/mongodb-org-5.0.list \
    && apt-get update \
    && apt-get install --no-install-recommends --yes \
        mongodb-org-shell \
        redis-tools \
        python3-pip \
        python3-dev \
        unixodbc-dev

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --requirement requirements.txt

COPY profiler.py .

ENTRYPOINT [ "python3" ]
CMD [ "./profiler.py" ]
