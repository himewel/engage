from pyspark.sql.functions import col
from pyspark.sql.types import StructField, StringType, IntegerType

from . import AbstractSchema


class GroupsSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("groupid", IntegerType()),
            StructField("name", StringType()),
        ]
        return schema
