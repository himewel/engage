from pyspark.sql.types import StructField, StringType, IntegerType, DoubleType

from . import AbstractSchema


class ActivitiesSchema(AbstractSchema):
    def get_column_names(self):
        column_names = ["activityId", "roundId", "activityWeight"]
        return column_names

    def get_schema(self):
        schema = [
            StructField("activityId", IntegerType(), True),
            StructField("roundId", IntegerType(), True),
            StructField("activityWeight", DoubleType(), True),
        ]
        return schema
