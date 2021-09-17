from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
)

from . import AbstractSchema


class AnswersSchema(AbstractSchema):
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
