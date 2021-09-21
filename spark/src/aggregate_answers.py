import os

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, collect_list, lit, struct, to_json

from schemas import (
    ActivitiesSchema,
    AnswersSchema,
    GroupsSchema,
    RoundsSchema,
    UsersSchema,
)

schemas = {
    "engagedb.dbo.activities": ActivitiesSchema(),
    "engagedb.dbo.answers": AnswersSchema(),
    "engagedb.dbo.groups": GroupsSchema(),
    "engagedb.dbo.rounds": RoundsSchema(),
    "engagedb.dbo.users": UsersSchema(),
}


def get_spark():
    context = SparkContext.getOrCreate()
    context.setLogLevel("WARN")
    spark = SQLContext(context)
    return spark


def transform(df, topic_list):
    for column in ["key", "value"]:
        df = df.withColumn(column, col(column).cast("string"))

    topic_dfs = {}
    for topic_name in topic_list:
        topic_df = df.where(col("topic") == topic_name)
        topic_df = schemas[topic_name].explode(
            dataframe=topic_df,
            src_column="value",
            dst_column="payload",
        )

        topic_df = topic_df.select("payload.after.*", "timestamp")
        topic_dfs[topic_name] = topic_df

    df = (
        topic_dfs["engagedb.dbo.answers"]
        .join(topic_dfs["engagedb.dbo.activities"], "activityId")
        .join(topic_dfs["engagedb.dbo.users"], "userId")
        .join(topic_dfs["engagedb.dbo.groups"], "groupId")
        .join(topic_dfs["engagedb.dbo.rounds"], "roundId")
    )

    for topic_name in topic_list:
        column_names = schemas[topic_name].get_column_names()
        id_column = schemas[topic_name].get_columnid()

        if id_column:
            column_names.append("_id")
            df = df.withColumn("_id", col(id_column))

        col_struct = struct([col(column) for column in column_names])
        df = df.withColumn(topic_name.split(".")[-1], col_struct)

    all_columns = [item.get_column_names() for _, item in schemas.items()]
    all_columns.append(["_id"])
    df = df.drop(*sum(all_columns, []))

    df = (
        df.withColumn("dummyWatermark", lit(1632174835).cast("timestamp"))
        .withWatermark("dummyWatermark", "100 years")
        .groupBy(col("dummyWatermark"), col("users"), col("rounds"), col("activities"))
        .agg(collect_list("answers").alias("answers"))
        .withColumn("activities", struct(col("activities.*"), col("answers")))
        .drop("answers", "dummyWatermark")
        .withColumn("value", to_json(struct(col("*"))))
        .select("value")
    )

    df.printSchema()

    return df


def get_process(broker_server, topic_list):
    spark = get_spark()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", broker_server)
        .option("subscribe", ",".join(topic_list))
        .option("startingOffsets", "earliest")
        .load()
    )

    df = transform(df, topic_list)

    process = (
        df.writeStream.trigger(processingTime="5 second")
        .format("kafka")
        .option("kafka.bootstrap.servers", broker_server)
        .option("topic", "aggregate_answers")
        .option("checkpointLocation", "/checkpoint/aggregate_answers")
        .start()
    )

    return process


if __name__ == '__main__':
    broker_server = os.getenv("BROKER_HOSTNAME")
    table_list = ["groups", "users", "activities", "answers", "rounds"]
    topic_list = [f"engagedb.dbo.{table}" for table in table_list]

    process = get_process(broker_server, topic_list)
    process.awaitTermination()
