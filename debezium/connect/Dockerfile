FROM debezium/connect:1.6

USER root

RUN yum install -y nc \
    && yum clean all

USER kafka

COPY ./wait-for-kafka.sh /
COPY ./create-connector.sh /
COPY ./connectors /connectors

ENTRYPOINT [ "/bin/bash", "/wait-for-kafka.sh" ]
