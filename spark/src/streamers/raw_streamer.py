from pyspark.sql.functions import col, from_unixtime

from . import AbstractStreamer


class RawStreamer(AbstractStreamer):
    def __init__(self, broker_server, topic_name):
        super().__init__()
        self.broker_server = broker_server
        self.topic_name = topic_name
        self.schema = self.schema_classes[topic_name]

    def get_process(self):
        spark = self.get_spark()

        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", self.broker_server)
            .option("subscribe", self.topic_name)
            .option("startingOffsets", "earliest")
            .load()
        )

        for column in ["key", "value"]:
            df = df.withColumn(column, col(column).cast("string"))

        df = self.schema.explode(
            dataframe=df, src_column="value", dst_column="payload"
        ).select("payload.after.*", "timestamp")

        long_columns = [field[0] for field in df.dtypes if field[1] == "bigint"]
        for column in long_columns:
            df = df.withColumn(
                column, from_unixtime(col(column) / 1000).cast("timestamp")
            )

        process = (
            df.coalesce(1)
            .writeStream.queryName(f"raw_{self.topic_name}")
            .option("checkpointLocation", f"file:///checkpoint/raw/{self.topic_name}")
            .start(path=f"/raw/{self.topic_name}")
        )

        return process

    def create_factory(broker_server):
        table_list = ["groups", "users", "activities", "answers", "rounds"]
        topic_list = [f"engagedb.dbo.{table}" for table in table_list]

        for topic_name in topic_list:
            streamer = RawStreamer(broker_server, topic_name)
            streamer.get_process()

        streamer.stream()
