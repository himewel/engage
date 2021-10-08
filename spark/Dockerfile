FROM python:3.8-slim

ENV HADOOP_HOME "/opt/hadoop"
ENV HADOOP_CONF_DIR "/etc/hadoop"
ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
ENV SPARK_HOME "/opt/spark"
ENV SPARK_NO_DAEMONIZE TRUE

ENV PATH "${PATH}:${JAVA_HOME}/bin:${SPARK_HOME}/bin:${SPARK_HOME}/sbin"
ENV PATH "${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"
ENV PATH "${PATH}:/home/spark/.local/bin"
ENV PYTHONPATH "${SPARK_HOME}/python:${PYTHONPATH}"

RUN mkdir -p /usr/share/man/man1 \
    && apt-get update \
    && apt-get install --no-install-recommends --yes \
        default-jdk \
        wget \
        netcat \
    && apt-get remove --purge ${builds_deps} \
    && apt-get clean \
    && rm -rf -- /var/lib/apt/lists/*

RUN wget -q https://ftp.unicamp.br/pub/apache/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz \
    && tar -xf hadoop-3.2.2.tar.gz \
    && rm -rf hadoop-3.2.2.tar.gz \
    && mv hadoop-3.2.2 ${HADOOP_HOME}

RUN wget -q https://ftp.unicamp.br/pub/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
    && tar -xf spark-3.1.2-bin-hadoop3.2.tgz \
    && rm -rf spark-3.1.2-bin-hadoop3.2.tgz \
    && mv spark-3.1.2-bin-hadoop3.2 ${SPARK_HOME} \
    && echo "log4j.appender.FILE.layout.conversionPattern=%m%n" >> ${SPARK_HOME}/conf/log4j.properties

WORKDIR ${SPARK_HOME}

COPY scripts ./scripts

RUN useradd -m spark \
    && mkdir -p /raw /checkpoint /trusted /refined \
    && chown spark /raw /checkpoint /trusted /refined \
    && chmod +x ./scripts/*.sh \
    && echo "export HADOOP_CONF_DIR=${HADOOP_CONF_DIR}" >> ${SPARK_HOME}/conf/spark-env.sh

USER spark

COPY requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir --requirement ./requirements.txt \
    && echo "exit()" >> ./spark_packages.py \
    && spark-submit --packages \
        org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        ./spark_packages.py \
    && rm -rf ./install_packages.py

COPY ./config ${HADOOP_CONF_DIR}
COPY ./src ./src

ENTRYPOINT [ "/bin/bash", "./scripts/spark-start.sh" ]
