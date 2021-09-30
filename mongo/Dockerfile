FROM mongo:5.0.2

COPY scripts ./scripts

RUN mkdir -p /mongo-storage

CMD [ "bash", "./scripts/wait-for-replica.sh"]
