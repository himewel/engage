from datetime import datetime

import numpy as np
from pymongo import MongoClient
from redis import Redis
from sqlalchemy import create_engine

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
            try:
                start_time = datetime.now()
                parameters["method"](parameters["engine"])
                end_time = datetime.now()
                time_list.append((end_time - start_time).microseconds)
            except:
                print("Falha buscando", name)
                break

        np_time_list = np.array(time_list)
        print(name, np_time_list.mean(), np_time_list.std())


def run_mssql(engine):
    query = """
        SELECT
            roundScores.userId,
            roundScores.roundId,
            roundScores.roundName,
            roundScores.roundScore,
            users.userName,
            users.groupId,
            RANK() OVER(
                PARTITION BY roundScores.roundId
                ORDER BY roundScore DESC) AS ranking
        FROM (
            SELECT
                activityScores.userId,
                activityScores.roundId,
                rounds.roundName,
                ISNULL(rounds.roundScoreBonus * (
                        activityScores.sumScores /
                        NULLIF(activityScores.sumWeights, 0)
                    ), 0) AS roundScore
            FROM (
                SELECT
        		    answers.userId,
        		    activities.roundId,
        		    SUM(activities.activityWeight) AS sumWeights,
        		    SUM(activityWeight * maxScore) AS sumScores
        		FROM engagedb.dbo.activities AS activities
        		JOIN (
        				SELECT userId, activityId, MAX(scoreOfAccuracy) AS maxScore
        				FROM engagedb.dbo.answers
        				GROUP BY userId, activityId
        			) AS answers
        		    ON answers.activityId = activities.activityId
        		GROUP BY
        			answers.userId,
        			activities.activityId,
        			activities.roundId
            ) activityScores
            JOIN engagedb.dbo.rounds AS rounds
                ON rounds.roundId = activityScores.roundId
        ) AS roundScores
        JOIN engagedb.dbo.users AS users
            ON users.userId = roundScores.userId
    """

    table = list(engine.execute(query))


def run_mongo(mongo):
    collection = list(mongo.engagedb.userScores.find({}, {"_id": 1, "rank": 1}))


def run_redis(redis):
    redis.keys("userScores:*")


if __name__ == '__main__':
    main()
