IF NOT EXISTS (SELECT *
               FROM   sys.databases
               WHERE  NAME = 'engagedb')
  BEGIN
      CREATE DATABASE engagedb;
  END

go

USE engagedb;

-- GROUPS
IF NOT EXISTS (SELECT *
               FROM   sys.tables t
                      JOIN sys.schemas s
                        ON t.schema_id = s.schema_id
               WHERE  s.NAME = 'dbo'
                      AND t.NAME = 'groups')
  BEGIN
      CREATE TABLE dbo.groups
        (
           groupId   INTEGER NOT NULL PRIMARY KEY,
           groupName VARCHAR(300)
        );
  END
ELSE
  BEGIN
      TRUNCATE TABLE dbo.groups;
  END

-- USERS
IF NOT EXISTS (SELECT *
               FROM   sys.tables t
                      JOIN sys.schemas s
                        ON t.schema_id = s.schema_id
               WHERE  s.NAME = 'dbo'
                      AND t.NAME = 'users')
  BEGIN
      CREATE TABLE dbo.users
        (
           userId   INTEGER NOT NULL PRIMARY KEY,
           groupId  INTEGER NOT NULL FOREIGN KEY REFERENCES groups(groupId),
           image    VARCHAR(300),
           username VARCHAR(300),
        );
  END
ELSE
  BEGIN
      TRUNCATE TABLE dbo.users;
  END

-- ROUNDS
IF NOT EXISTS (SELECT *
               FROM   sys.tables t
                      JOIN sys.schemas s
                        ON t.schema_id = s.schema_id
               WHERE  s.NAME = 'dbo'
                      AND t.NAME = 'rounds')
  BEGIN
      CREATE TABLE dbo.rounds
        (
           roundId         INTEGER NOT NULL PRIMARY KEY,
           name            VARCHAR(300),
           roundscorebonus INTEGER,
        );
  END
ELSE
  BEGIN
      TRUNCATE TABLE dbo.rounds;
  END

-- ACTIVITIES
IF NOT EXISTS (SELECT *
               FROM   sys.tables t
                      JOIN sys.schemas s
                        ON t.schema_id = s.schema_id
               WHERE  s.NAME = 'dbo'
                      AND t.NAME = 'activities')
  BEGIN
      CREATE TABLE dbo.activities
        (
           activityId     INTEGER NOT NULL PRIMARY KEY,
           roundId        INTEGER NOT NULL FOREIGN KEY REFERENCES rounds(roundId),
           activityweight FLOAT
        );
  END
ELSE
  BEGIN
      TRUNCATE TABLE dbo.activities;
  END

-- ANSWERS
IF NOT EXISTS (SELECT *
               FROM   sys.tables t
                      JOIN sys.schemas s
                        ON t.schema_id = s.schema_id
               WHERE  s.NAME = 'dbo'
                      AND t.NAME = 'answers')
  BEGIN
      CREATE TABLE dbo.answers
        (
           activityId      INTEGER NOT NULL FOREIGN KEY REFERENCES activities(activityId),
           userId          INTEGER NOT NULL FOREIGN KEY REFERENCES users(userId),
           scoreofaccuracy FLOAT,
           answerdatetime  DATETIME,
           approved        VARCHAR(5)
        );
  END
ELSE
  BEGIN
      TRUNCATE TABLE dbo.users;
  END

-- enable CDC
IF NOT EXISTS(SELECT *
              FROM   sys.databases
              WHERE  is_cdc_enabled = 1
                     AND NAME = 'engagedb')
  BEGIN
      EXEC sys.Sp_cdc_enable_db;
  END
