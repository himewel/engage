FROM debezium/kafka:1.6

USER root

RUN yum install -y nc \
    && yum clean all

USER kafka

COPY ./wait-for-zookeeper.sh /

ENTRYPOINT ["/bin/bash"]
CMD ["/wait-for-zookeeper.sh"]
