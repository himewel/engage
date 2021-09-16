from pyspark.sql.types import StructField, StringType, IntegerType

from . import AbstractSchema


class UsersSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("userid", IntegerType()),
            StructField("groupid", IntegerType()),
            StructField("name", StringType()),
            StructField("image", StringType()),
        ]
        return schema
