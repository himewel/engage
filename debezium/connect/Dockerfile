FROM debezium/connect:1.6

USER root

RUN yum install -y nc \
    && yum clean all

USER kafka

COPY ./wait-for-kafka.sh /

ENTRYPOINT ["/bin/bash"]
CMD ["/wait-for-kafka.sh"]
