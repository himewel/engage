import json
import logging
from datetime import datetime

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from redis import Redis


class CacheStreamer:
    def __init__(self, broker_server, linstening_topic_name, speaking_topic_name):
        self.broker_server = broker_server
        self.linstening_topic_name = linstening_topic_name
        self.speaking_topic_name = speaking_topic_name

    def start_poll(self):
        logging.info("Creating kafka consumer")
        consumer = KafkaConsumer(
            bootstrap_servers=self.broker_server,
            auto_offset_reset="earliest",
        )
        consumer.subscribe(topics=[self.linstening_topic_name])

        while True:
            message_pack = consumer.poll(timeout_ms=500)
            if not message_pack:
                continue

            for topic, message_list in message_pack.items():
                for message in message_list:
                    timestamp = datetime.fromtimestamp(message.timestamp / 1000)
                    logging.info(f"New message received from {topic}")
                    logging.info(f"Timestamp: {timestamp}")
                    logging.info(f"Offset: {message.offset}")
                    logging.info(f"Value: {message.value}")

            self.migrate_mongo_to_redis()
            self.send_event()

    def migrate_mongo_to_redis(self):
        logging.info("Getting mongodb client...")
        mongo = MongoClient("mongodb://debezium:debezium@mongodb:27017")
        redis = Redis(host="redis", port=6379, db=0)

        collection_list = ["userScores", "groupScores"]
        for collection in collection_list:
            logging.info(f"Deleting old values for {collection}...")
            redis.delete(f"{collection}:*")

            logging.info(f"Searching for {collection} aggregation...")
            for document in mongo.engagedb[collection].find().limit(100):
                id = self.get_documentid(collection, document)
                logging.info(f"Inserting {id} into redis...")

                for key, item in document.items():
                    field = (
                        json.dumps(item).encode("utf-8")
                        if isinstance(item, dict)
                        else item
                    )
                    redis.hset(name=id, key=key, value=field)

    def send_event(self):
        producer = KafkaProducer(bootstrap_servers=self.broker_server)
        producer.send(topic=self.speaking_topic_name, value=b"Fresh aggregations")

    def get_documentid(self, collection, document):
        if collection == "userScores":
            id = (
                f"{collection}:{document['_id']['roundId']}"
                f":{document['rank']}:{document['_id']['userId']}"
            )
        elif collection == "groupScores":
            id = f"{collection}:{document['rank']}:{document['_id']['groupId']}"
        return id

    def create_factory(broker_server):
        linstening_topic_name = "mongo.scores"
        speaking_topic_name = "redis.cache"

        streamer = CacheStreamer(
            broker_server=broker_server,
            linstening_topic_name=linstening_topic_name,
            speaking_topic_name=speaking_topic_name,
        )
        streamer.start_poll()
