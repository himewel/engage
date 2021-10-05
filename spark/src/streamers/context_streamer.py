import json
import logging
from collections import OrderedDict
from datetime import datetime

from kafka import KafkaConsumer
from pymongo import MongoClient


class ContextStreamer:
    def __init__(self, broker_server, topic_name):
        self.broker_server = broker_server
        self.topic_name = topic_name

    def start_poll(self):
        logging.info("Creating kafka consumer")
        consumer = KafkaConsumer(
            bootstrap_servers=self.broker_server,
            auto_offset_reset="earliest",
        )
        consumer.subscribe(topics=[self.topic_name])

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

            self.update_mongo()

    def update_mongo(self):
        mongo = MongoClient("mongodb://debezium:debezium@mongodb:27017")

        aggregations = [
            ("activity_scores", mongo.engagedb.activities),
            ("round_scores", mongo.engagedb.rounds),
            ("user_scores", mongo.engagedb.users),
            ("group_scores", mongo.engagedb.userScores),
        ]

        for file, db in aggregations:
            with open(f"/opt/spark/src/queries/{file}.json") as stream:
                pipeline = json.load(stream, object_pairs_hook=OrderedDict)

            logging.info(f"Applying {file} aggregation...")
            db.aggregate(pipeline)

    def create_factory(broker_server):
        topic_name = "spark.answers"
        streamer = ContextStreamer(broker_server, topic_name)
        streamer.start_poll()
