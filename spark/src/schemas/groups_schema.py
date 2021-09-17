from pyspark.sql.functions import col
from pyspark.sql.types import StructField, StringType, IntegerType

from . import AbstractSchema


class GroupsSchema(AbstractSchema):
    def get_column_names(self):
        column_names = ["groupId", "groupName"]
        return column_names

    def get_schema(self):
        schema = [
            StructField("groupId", IntegerType(), True),
            StructField("groupName", StringType(), True),
        ]
        return schema
