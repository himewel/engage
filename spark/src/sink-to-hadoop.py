import os

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.streaming import StreamingQueryManager
from pyspark.sql.functions import col, date_format


def get_spark():
    context = SparkContext.getOrCreate()
    spark = SQLContext(context)
    return spark


def transform(df):
    for column in ["key", "value"]:
        df = df.withColumn(column, col(column).cast("string"))

    df = (
        df.withColumn("year", date_format(col("timestamp"), "yyyy"))
        .withColumn("month", date_format(col("timestamp"), "MM"))
        .withColumn("day", date_format(col("timestamp"), "dd"))
    )
    return df


def start_stream(broker_server, topic_name):
    spark = get_spark()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", broker_server)
        .option("subscribe", topic_name)
        .option("startingOffsets", "earliest")
        .load()
    )

    df = transform(df)

    process = df.writeStream.trigger(processingTime="5 second").start(
        path=f"/landing/{topic_name}",
        checkpointLocation=f"/checkpoint/landing/{topic_name}",
        mode="append",
        partitionBy=["year", "month", "day"],
    )

    return process


if __name__ == '__main__':
    broker_server = os.getenv("BROKER_HOSTNAME")
    table_list = ["groups", "users", "activities", "answers", "rounds"]
    topic_list = [f"engagedb.dbo.{table}" for table in table_list]

    for topic_name in table_list:
        process = start_stream(broker_server, topic_name)

    spark = get_spark()
    spark.streams.awaitAnyTermination()
