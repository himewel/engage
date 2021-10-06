FROM mongo:5.0

COPY scripts ./scripts

RUN mkdir -p /mongo-storage /var/log/mongodb

ENTRYPOINT [ "/bin/bash", "./scripts/init-replica.sh" ]
