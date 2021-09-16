from pyspark.sql.types import (
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType,
)

from . import AbstractSchema


class AnswersSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("activityid", IntegerType()),
            StructField("userid", IntegerType()),
            StructField("scoreofaccuracy", DoubleType()),
            StructField("answerdatetime", TimestampType()),
            StructField("approved", StringType()),
        ]
        return schema
