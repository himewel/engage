FROM python:3.8-slim

ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
ENV SPARK_HOME "/opt/spark"
ENV HADOOP_CONF_DIR "/etc/hadoop"
ENV PATH "${PATH}:${JAVA_HOME}/bin:${SPARK_HOME}/bin:${SPARK_HOME}/sbin"
ENV PYTHONPATH "${SPARK_HOME}/python:${PYTHONPATH}"
ENV SPARK_NO_DAEMONIZE TRUE

RUN mkdir -p /usr/share/man/man1 \
    && apt-get update \
    && apt-get install --no-install-recommends --yes \
        default-jdk \
        wget \
        netcat \
    && apt-get remove --purge ${builds_deps} \
    && apt-get clean \
    && rm -rf -- /var/lib/apt/lists/*

RUN wget -q https://ftp.unicamp.br/pub/apache/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
    && tar -xf spark-3.1.2-bin-hadoop3.2.tgz \
    && rm -rf spark-3.1.2-bin-hadoop3.2.tgz \
    && mv spark-3.1.2-bin-hadoop3.2 ${SPARK_HOME} \
    && echo "log4j.appender.FILE.layout.conversionPattern=%m%n" >> ${SPARK_HOME}/conf/log4j.properties

WORKDIR ${SPARK_HOME}

COPY start.sh ./start.sh

RUN useradd -m spark \
    && mkdir -p /raw /checkpoint \
    && chown spark /raw /checkpoint \
    && chmod +x ./start.sh \
    && echo "export HADOOP_CONF_DIR=${HADOOP_CONF_DIR}" >> ${SPARK_HOME}/conf/spark-env.sh

USER spark

RUN pip3 install --no-cache-dir pyspark==3.1.2

ENTRYPOINT [ "/bin/bash", "./start.sh" ]
