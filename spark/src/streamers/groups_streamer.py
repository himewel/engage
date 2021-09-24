from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType

from . import AbstractStreamer


class GroupsStreamer(AbstractStreamer):
    def __init__(self, table_list):
        super().__init__()
        self.table_list = table_list

    def get_process(self):
        spark = self.get_spark()

        df_list = {}
        for table in self.table_list:
            schema_name = f"engagedb.dbo.{table}"
            schema_fields = self.schema_classes[schema_name].get_raw_schema()

            path = f"/trusted/{table}"
            schema = StructType(schema_fields)
            df_list[table] = self.read_dataframe_with_delay(
                spark.readStream, path, schema
            )

        df = (
            df_list["answers"]
            .join(df_list["activities"], "activityId")
            .withColumn("score", col("scoreOfAccuracy") * col("activityWeight"))
            .join(df_list["rounds"], "roundId")
            .withColumn("watermark", lit(1632174835).cast("timestamp"))
            .withWatermark("watermark", "100 years")
            .groupBy(
                col("watermark"),
                col("userId"),
                col("roundId"),
                col("roundScoreBonus"),
            )
            .agg({"score": "sum", "activityWeight": "sum"})
            .withColumn(
                "roundScore",
                col("roundScoreBonus") * col("sum(score)") / col("sum(activityWeight)"),
            )
            .drop("watermark", "sum(score)", "sum(activityWeight)")
        )

        process = (
            df.coalesce(1)
            .writeStream.queryName(f"refined_groups_ranking")
            .format("console")
            .outputMode("append")
            .option("checkpointLocation", "file:///checkpoint/refined/groups_ranking")
            .start()
        )

        return process

    def create_factory():
        table_list = ["activities", "answers", "rounds"]

        streamer = GroupsStreamer(table_list)
        streamer.get_process()
        streamer.stream()
