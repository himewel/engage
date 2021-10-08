from datetime import datetime

from sqlalchemy import create_engine
from pymongo import MongoClient
from redis import Redis

_LOOP_LIMIT = 10000


def main():
    databases = {
        "mssql": {
            "method": run_mssql,
            "engine": create_engine(
                "mssql+pyodbc://sa:SuperP4ssword!@mssql:1433/engagedb"
                "?driver=ODBC+Driver+17+for+SQL+Server"
            ),
        },
        "mongo": {
            "method": run_mongo,
            "engine": MongoClient("mongodb://debezium:debezium@mongodb:27017"),
        },
        "redis": {"method": run_redis, "engine": Redis(host="redis", db=0)},
    }

    for name, parameters in databases.items():
        time_list = []
        for _ in range(_LOOP_LIMIT):
            start_time = datetime.now()
            parameters["method"](parameters["engine"])
            end_time = datetime.now()
            time_list.append((end_time - start_time).microseconds)
        print(name, sum(time_list) / len(time_list))


def run_mssql(engine):
    table = list(
        engine.execute(
            """
            SELECT users.userId, userName, groupName, roundName,
                roundScoreBonus, activityWeight, scoreOfAccuracy
            FROM engagedb.dbo.users AS users
            JOIN engagedb.dbo.groups AS groups
                ON users.groupId = groups.groupId
            JOIN engagedb.dbo.answers AS answers
                ON answers.userId = users.userId
            JOIN engagedb.dbo.activities AS activities
                ON activities.activityId = answers.activityId
            JOIN engagedb.dbo.rounds AS rounds
                ON rounds.roundId = activities.roundId
            """
        )
    )


def run_mongo(mongo):
    collection = list(mongo.engagedb.userScores.find({}, {"_id": 1, "rank": 1}))


def run_redis(redis):
    redis.keys("userScores:*")


if __name__ == '__main__':
    main()
