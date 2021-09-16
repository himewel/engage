from pyspark.sql.functions import col
from pyspark.sql.types import StructField, StringType, IntegerType, DoubleType

from . import AbstractSchema


class RoundsSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("roundid", IntegerType()),
            StructField("name", StringType()),
            StructField("roundscorebonus", DoubleType()),
        ]
        return schema
