from pyspark.sql.functions import col
from pyspark.sql.types import StructField, StringType, IntegerType, DoubleType

from . import AbstractSchema


class RoundsSchema(AbstractSchema):
    def get_column_names(self):
        column_names = ["roundId", "roundName", "roundScoreBonus"]
        return column_names

    def get_schema(self):
        schema = [
            StructField("roundId", IntegerType(), True),
            StructField("roundName", StringType(), True),
            StructField("roundScoreBonus", DoubleType(), True),
        ]
        return schema
