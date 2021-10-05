from pyspark.sql.functions import col, concat, from_unixtime

from . import AbstractStreamer


class RawStreamer(AbstractStreamer):
    def __init__(self, broker_server, topic_name):
        super().__init__()
        self.broker_server = broker_server
        self.topic_name = topic_name
        self.table_name = topic_name.split(".")[-1]
        self.schema = self.schema_classes[topic_name]

    def multipleWriteFormats(self, batch_df, batch_id):
        hdfs_process = (
            batch_df.write.format("parquet")
            .mode("append")
            .save(f"/raw/{self.table_name}")
        )
        mongo_process = (
            batch_df.write.format("mongo")
            .mode("append")
            .option("uri", "mongodb://debezium:debezium@mongodb:27017")
            .option("database", "engagedb")
            .option("collection", self.table_name)
            .save()
        )

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

        column_id = [col(column) for column in self.schema.get_columnid()]
        if len(column_id) == 1:
            df = df.withColumn("_id", *column_id)
        else:
            df = df.withColumn("_id", concat(*column_id, col("timestamp").cast("long")))

        process = (
            df.writeStream.queryName(f"raw_{self.topic_name}")
            .foreachBatch(self.multipleWriteFormats)
            .option("checkpointLocation", f"file:///checkpoint/raw/{self.topic_name}")
            .start()
        )

        return process

    def create_factory(broker_server):
        table_list = ["groups", "users", "activities", "answers", "rounds"]
        topic_list = [f"engagedb.dbo.{table}" for table in table_list]

        for topic_name in topic_list:
            streamer = RawStreamer(broker_server, topic_name)
            streamer.get_process()

        streamer.stream()
