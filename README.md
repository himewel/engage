# Engage Challenge

<p>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="SQL Server" src="https://img.shields.io/badge/microsoftsqlserver-%23cc2927.svg?&style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>
<img alt="Apache Spark" src="https://img.shields.io/badge/apachespark-%23E25A1C.svg?&style=for-the-badge&logo=apachespark&logoColor=white"/>
<img alt="MongoDB" src="https://img.shields.io/badge/mongodb-%2347A248.svg?&style=for-the-badge&logo=mongodb&logoColor=white"/>
<img alt="Redis" src="https://img.shields.io/badge/redis-%23DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
</p>

<p align="center">
<img alt="Architecture" src="./docs/architecture.png"/>
</p>

This project implements a NoSQL strategy to optimize queries executed on a SQL Server. To do it, the presented architecture was built. A rest API is available as a data source to create our SQL Server replication. The NoSQL databases are populated with data extracted from the SQL Server with Debezium and structured with Spark. In the end, MongoDB is used as main database for the query executions and Redis serve as cache to store the main results. In short:

- Debezium: kafka based solution for CDC monitoring from SQL Server;
- Hadoop: long term data solution, used to append data in parquet format;
- MongoDB: main NoSQL storage for the solution;
- Redis: in memory database used to cache the main query results from MongoDB;
- Spark: used to stream data from Debezium, transform and ingest data in the leafs: Hadoop, MongoDB and Redis;
- SQL Server: data source where transactional data is stored;

In principle, our SQL Server replica is built as the following schema.

<p align="center">
<img alt="Schema" src="./docs/schema.png" width=70%/>
</p>

## How to start

All the code developed is structured in docker containers and docker compose files. As the containers are divided in multiple compose files, the Makefile targets should help to manipulate it.

First of all, `make init` creates the necessary docker requirements. So, to start the containers, `make init` should be run first. Implicitly it is already called before `storage`, `debezium`, `streaming` and `all` targets. In example, to start only the storage containers such as Hadoop, SQL Server, Redis and MongoDB:

```shell
make storage
```

To start only the Debezium services such as Kafka, Zookeeper and Debezium Connect:

```shell
make debezium
```

To start only the Spark jobs such as Hadoop, MongoDB and Redis ingestions:

```shell
make streaming
```

To start all the containers:

```shell
make all

# to stop them
make stop
```

## Data flow

A spark streaming job is triggered to each topic from SQL Server CDC and extract the data to be inserted in hdfs and MongoDB. In this layer, the data inserts occurs as the following: hdfs only append the data extracted in hadoop partitioned by extraction time; as MongoDB replace documents with same \_id, all the rows from SQL Server are upserted.

<p align="center">
<img alt="Dataflow" src="./docs/dataflow.png"/>
</p>

The second layer runs only when the first layer insert new data and trigger a Kafka event (spark.answers). This layer is responsible to calculate the rank aggregations in MongoDB. To do it, some auxiliar collections are merged running lookup and group aggregations. The third layer also runs oriented by Kafka events (mongo.scores). In this layer, the aggregations created in the second layer are collected and transformed to be available in Redis.

## User interface endpoints

- Hadoop WebHDFS: http://localhost:9870
- Kafka Control Center: http://localhost:9021
- Spark (raw jobs): http://localhost:4040
