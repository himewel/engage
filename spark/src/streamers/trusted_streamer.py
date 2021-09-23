from time import sleep

from pyspark.sql.functions import col, row_number
from pyspark.sql.types import StructType
from pyspark.sql.utils import AnalysisException
from pyspark.sql.window import Window

from . import AbstractStreamer


class TrustedStreamer(AbstractStreamer):
    def __init__(self, topic_name):
        super().__init__()
        self.topic_name = topic_name
        self.table_name = topic_name.split(".")[-1]
        self.schema = self.schema_classes[self.topic_name]

    def upsert(self, batch_df, batch_id):
        spark = self.get_spark()
        schema_fields = self.schema.get_raw_schema()
        try:
            old_df = spark.read.format("parquet").load(
                path=f"/trusted/{self.table_name}",
                schema=StructType(schema_fields),
            )
        except AnalysisException:
            old_df = spark.createDataFrame([], StructType(schema_fields))

        column_ids = self.schema.get_columnid()
        orderby_columns = self.schema.get_orderby()

        window = Window.partitionBy(*column_ids).orderBy(*orderby_columns)
        batch_df = (
            batch_df.union(old_df)
            .withColumn("ranking", row_number().over(window))
            .where(col("ranking") == 1)
            .drop("ranking")
            .write.format("parquet")
            .mode("overwrite")
            .save(path=f"/trusted/{self.table_name}")
        )

    def get_process(self):
        spark = self.get_spark()

        schema_fields = self.schema.get_raw_schema()
        try:
            df = spark.readStream.format("parquet").load(
                path=f"/raw/{self.topic_name}",
                schema=StructType(schema_fields),
            )
        except AnalysisException:
            sleep(30)
            df = spark.readStream.format("parquet").load(
                path=f"/raw/{self.topic_name}",
                schema=StructType(schema_fields),
            )

        process = (
            df.writeStream.queryName(f"trusted_{self.table_name}")
            .foreachBatch(self.upsert)
            .option("checkpointLocation", f"/checkpoint/trusted/{self.table_name}")
            .start()
        )

        return process

    def create_factory():
        table_list = ["groups", "users", "activities", "answers", "rounds"]
        topic_list = [f"engagedb.dbo.{table}" for table in table_list]

        for topic_name in topic_list:
            streamer = TrustedStreamer(topic_name)
            streamer.get_process()

        streamer.stream()
