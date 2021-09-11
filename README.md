# Engage Challenge

<p>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="SQL Server" src="https://img.shields.io/badge/microsoftsqlserver-%23cc2927.svg?&style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>
<img alt="Apache Spark" src="https://img.shields.io/badge/apachespark-%23E25A1C.svg?&style=for-the-badge&logo=apachespark&logoColor=white"/>
<img alt="MongoDB" src="https://img.shields.io/badge/mongodb-%2347A248.svg?&style=for-the-badge&logo=mongodb&logoColor=white"/>
<img alt="Redis" src="https://img.shields.io/badge/redis-%23DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
</p>

This project implements a NoSQL strategy to optimize queries executed on a SQL Server. To do it, the following architecture was built. A rest API is available as a data source to create our SQL Server replication. The NoSQL databases are populated with data extracted from the SQL Server with Debezium and structured with Spark. In the end, MongoDB is used as main database for the query executions and Redis serve as cache to store the main results.

<p align="center">
<img alt="Architecture" src="./docs/architecture.png"/>
</p>

In principle, our SQL Server replica is built as the following.

<p align="center">
<img alt="Schema" src="./docs/schema.png"/>
</p>
