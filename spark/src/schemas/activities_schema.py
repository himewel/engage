from pyspark.sql.types import StructField, StringType, IntegerType, DoubleType

from . import AbstractSchema


class ActivitiesSchema(AbstractSchema):
    def get_schema(self):
        schema = [
            StructField("activityid", IntegerType()),
            StructField("roundid", IntegerType()),
            StructField("activityweight", DoubleType()),
        ]
        return schema
