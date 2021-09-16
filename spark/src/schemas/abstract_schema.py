from abc import ABC, abstractmethod

from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType


class AbstractSchema(ABC):
    @abstractmethod
    def get_schema(self):
        pass

    def convert(self, dataframe, source_column, destination_column):
        columns = self.get_schema()
        schema = StructType(columns)

        dataframe = dataframe.withColumn(
            destination_column, from_json(col(source_column), schema)
        )
        return dataframe
