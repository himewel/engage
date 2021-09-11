# Engage Challenge

This project implements a NoSQL strategy to optimize queries executed on a SQL Server. To do it, the following architecture was built. A rest API is available as a data source to create our SQL Server replication. The NoSQL databases are populated with data extracted from the SQL Server with Debezium and structured with Spark. In the end, MongoDB is used as main database for the query executions and Redis serve as cache to store the main results.

<p align="center">
<img alt="Architecture" src="./docs/architecture.png"/>
</p>

In principle, our SQL Server replica is built as the following.

<p align="center">
<img alt="Schema" src="./docs/schema.png"/>
</p>
