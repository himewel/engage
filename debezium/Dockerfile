FROM alpine:3.14

RUN apk add curl gcompat

COPY connectors ./connectors
COPY create-connector.sh .

CMD [ "sh", "./create-connector.sh"]
