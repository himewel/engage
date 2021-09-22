from abc import ABC, abstractmethod

from pyspark import SparkContext, SQLContext

from schemas import (
    ActivitiesSchema,
    AnswersSchema,
    GroupsSchema,
    RoundsSchema,
    UsersSchema,
)


class AbstractStreamer(ABC):
    def __init__(self):
        self.schema_classes = {
            "engagedb.dbo.activities": ActivitiesSchema(),
            "engagedb.dbo.answers": AnswersSchema(),
            "engagedb.dbo.groups": GroupsSchema(),
            "engagedb.dbo.rounds": RoundsSchema(),
            "engagedb.dbo.users": UsersSchema(),
        }

    @abstractmethod
    def get_process(self):
        pass

    def create_factory():
        pass

    def get_spark(self):
        context = SparkContext.getOrCreate()
        spark = SQLContext(context)
        return spark

    def stream(self):
        spark = self.get_spark()
        spark.streams.awaitAnyTermination()
