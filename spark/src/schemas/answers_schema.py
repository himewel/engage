from pyspark.sql.functions import col
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    TimestampType,
)

from . import AbstractSchema


class AnswersSchema(AbstractSchema):
    def get_columnid(self):
        return ["activityId", "userId"]

    def get_orderby(self):
        return [col("scoreOfAccuracy").desc(), col("timestamp").desc()]

    def get_raw_schema(self):
        schema = [
            StructField("activityId", IntegerType(), True),
            StructField("userId", IntegerType(), True),
            StructField("scoreOfAccuracy", DoubleType(), True),
            StructField("answerDatetime", TimestampType(), True),
            StructField("approved", StringType(), True),
            StructField("timestamp", TimestampType(), True),
        ]
        return schema

    def get_column_names(self):
        column_names = [
            "activityId",
            "userId",
            "scoreOfAccuracy",
            "answerDatetime",
            "approved",
        ]
        return column_names

    def get_schema(self):
        schema = [
            StructField("activityId", IntegerType(), True),
            StructField("userId", IntegerType(), True),
            StructField("scoreOfAccuracy", DoubleType(), True),
            StructField("answerDatetime", LongType(), True),
            StructField("approved", StringType(), True),
        ]
        return schema
