import os

from pyspark.sql.functions import col, date_format

from .abstract_streamer import AbstractStreamer


class RawStreamer(AbstractStreamer):
    def transform(self, df, topic_name):
        for column in ["key", "value"]:
            df = df.withColumn(column, col(column).cast("string"))

        df = self.schema_classes[topic_name].explode(
            dataframe=df,
            src_column="value",
            dst_column="payload",
        )

        df = (
            df.withColumn("year", date_format(col("timestamp"), "yyyy"))
            .withColumn("month", date_format(col("timestamp"), "MM"))
            .withColumn("day", date_format(col("timestamp"), "dd"))
        )
        return df

    def get_process(self, broker_server, topic_name):
        spark = self.get_spark()

        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", broker_server)
            .option("subscribe", topic_name)
            .option("startingOffsets", "earliest")
            .load()
        )

        df = self.transform(df, topic_name)

        process = (
            df.writeStream.trigger(processingTime="5 second")
            .queryName(f"subscribe_{topic_name}")
            .start(
                path=f"/raw/{topic_name}",
                checkpointLocation=f"/checkpoint/raw/{topic_name}",
                mode="append",
                partitionBy=["year", "month", "day"],
            )
        )

        return process

    def create_factory(broker_server):
        table_list = ["groups", "users", "activities", "answers", "rounds"]
        topic_list = [f"engagedb.dbo.{table}" for table in table_list]

        streamer = RawStreamer()
        for topic_name in topic_list:
            streamer.get_process(broker_server, topic_name)

        streamer.stream()
