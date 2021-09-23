from abc import ABC, abstractmethod

from pyspark.sql.functions import col, from_json, get_json_object
from pyspark.sql.types import LongType, StructField, StructType, StringType


class AbstractSchema(ABC):
    @abstractmethod
    def get_schema(self):
        pass

    @abstractmethod
    def get_column_names(self):
        pass

    @abstractmethod
    def get_columnid(self):
        pass

    def get_raw_schema(self):
        return self.get_schema() + [StructField("timestamp", LongType(), True)]

    def get_source_schema(self):
        source_schema = StructType(
            [
                StructField("version", StringType(), True),
                StructField("connector", StringType(), True),
                StructField("name", StringType(), True),
                StructField("ts_ms", LongType(), True),
                StructField("snapshot", StringType(), True),
                StructField("db", StringType(), True),
                StructField("sequence", StringType(), True),
                StructField("schema", StringType(), True),
                StructField("table", StringType(), True),
                StructField("change_lsn", StringType(), True),
                StructField("commit_lsn", StringType(), True),
                StructField("event_serial_no", LongType(), True),
            ]
        )
        return source_schema

    def get_transaction_schema(self):
        transaction_schema = StructType(
            [
                StructField("id", StringType(), True),
                StructField("total_order", LongType(), True),
                StructField("data_collection_order", LongType(), True),
            ]
        )
        return transaction_schema

    def get_payload_schema(self, table_schema):
        source_schema = self.get_source_schema()
        transaction_schema = self.get_transaction_schema()

        payload_schema = StructType(
            [
                StructField("before", table_schema, True),
                StructField("after", table_schema, True),
                StructField("source", source_schema, True),
                StructField("transaction", transaction_schema, True),
                StructField("op", StringType(), True),
                StructField("ts_ms", LongType(), True),
            ]
        )
        return payload_schema

    def explode(self, dataframe, src_column, dst_column):
        table_schema = StructType(self.get_schema())
        payload_schema = self.get_payload_schema(table_schema)

        dataframe = dataframe.withColumn(
            dst_column, get_json_object(col(src_column), "$.payload")
        ).withColumn(dst_column, from_json(col(dst_column), payload_schema))
        return dataframe
