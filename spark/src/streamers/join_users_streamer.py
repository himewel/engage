from . import AbstractStreamer


class JoinUsersStreamer(AbstractStreamer):
    def create_factory():
        table_list = ["groups", "users"]
        paths = {
            "groups": "/raw/engagedb.dbo.groups",
            "users": "/raw/engagedb.dbo.users",
        }

        streamer = JoinUsersStreamer()
        streamer.get_process(paths)
        streamer.stream()

    def read_parquet(self, path):
        spark = self.get_spark()

        df = spark.read.format("parquet").load(path=path)
        df = (
            spark.readStream.format("parquet")
            .load(path=path, schema=df.schema)
            .select("payload.after.*", "timestamp")
        )
        return df

    def upsert_batch(self, batch_df, batch_id):
        output_path = "/trusted/join_users_streamer"
        column_ids = [col("userId"), col("groupId")]
        old_df = spark.read.format("parquet").load(path=output_path)

        window = Window.partitionBy(*column_ids).orderBy(col("timestamp").desc())
        batch_df = (
            batch_df.union(old_df)
            .withColumn("ranking", row_number().over(window))
            .where(col("ranking") == 1)
            .drop("ranking")
        )

        _ = (
            batch_df.write.format("parquet")
            .option("path", output_path)
            .outputMode("overwrite")
            .save()
        )

    def get_process(self, paths):
        spark = self.get_spark()

        users_df = self.read_parquet(paths["users"])
        groups_df = self.read_parquet(paths["groups"])

        df = users_df.join(groups_df, "groupId")

        column_names = (
            self.schema_classes["engagedb.dbo.groups"].get_column_names()
            + self.schema_classes["engagedb.dbo.users"].get_column_names()
        )
        df = df.select(*column_names)

        process = (
            df.writeStream.trigger(processingTime="5 seconds")
            .foreachBatch(self.upsert_batch)
            .option("checkpointLocation", "/checkpoint/join_users_streamer")
            .start()
        )

        return process
