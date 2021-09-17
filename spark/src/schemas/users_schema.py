from pyspark.sql.types import StructField, StringType, IntegerType

from . import AbstractSchema


class UsersSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("userId", IntegerType(), True),
            StructField("groupId", IntegerType(), True),
            StructField("userName", StringType(), True),
            StructField("image", StringType(), True),
        ]
        return schema
