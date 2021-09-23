from pyspark.sql.functions import col, from_unixtime

from . import AbstractStreamer


class RawStreamer(AbstractStreamer):
    def get_process(self, broker_server, topic_name):
        spark = self.get_spark()

        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", broker_server)
            .option("subscribe", topic_name)
            .option("startingOffsets", "earliest")
            .load()
        )

        for column in ["key", "value"]:
            df = df.withColumn(column, col(column).cast("string"))

        df = (
            self.schema_classes[topic_name]
            .explode(dataframe=df, src_column="value", dst_column="payload")
            .select("payload.after.*", "timestamp")
        )

        long_columns = [field[0] for field in df.dtypes if field[1] == "bigint"]
        for column in long_columns:
            df = df.withColumn(column, from_unixtime(col(column) / 1000))

        process = df.writeStream.queryName(f"subscribe_{topic_name}").start(
            path=f"/raw/{topic_name}",
            checkpointLocation=f"/checkpoint/raw/{topic_name}",
            mode="append",
        )

        return process

    def create_factory(broker_server):
        table_list = ["groups", "users", "activities", "answers", "rounds"]
        topic_list = [f"engagedb.dbo.{table}" for table in table_list]

        streamer = RawStreamer()
        for topic_name in topic_list:
            streamer.get_process(broker_server, topic_name)

        streamer.stream()
