IF NOT EXISTS (
    SELECT *
    FROM sys.databases
    WHERE name = 'engagedb'
)
BEGIN
    CREATE DATABASE engagedb;
END
GO

USE engagedb;
EXEC sys.sp_cdc_disable_db;

-- GROUPS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'dbo' AND
        t.name = 'groups'
)
    BEGIN
        CREATE TABLE dbo.groups (
            groupId        INTEGER,
            groupName      VARCHAR(300)
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE dbo.groups;
    END

-- USERS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'dbo' AND
        t.name = 'users'
)
    BEGIN
        CREATE TABLE dbo.users (
            userId        INTEGER,
            groupId       INTEGER,
            image         VARCHAR(300),
            username      VARCHAR(300),
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE dbo.users;
    END

-- ROUNDS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'dbo' AND
        t.name = 'rounds'
)
BEGIN
        CREATE TABLE dbo.rounds (
            roundId               INTEGER,
            name                  VARCHAR(300),
            roundscorebonus       INTEGER,
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE dbo.rounds;
    END

-- ACTIVITIES
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'dbo' AND
        t.name = 'activities'
)
    BEGIN
        CREATE TABLE dbo.activities (
            activityid      INTEGER,
            roundid         INTEGER,
            activityweight  FLOAT
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE dbo.activities;
    END

-- ANSWERS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'dbo' AND
        t.name = 'answers'
)
    BEGIN
        CREATE TABLE dbo.answers (
            activityid          INTEGER,
            userid              INTEGER,
            scoreofaccuracy     FLOAT,
            answerdatetime      DATETIME,
            approved            VARCHAR(5)
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE dbo.users;
    END

-- enable CDC
IF NOT EXISTS(
    SELECT * FROM sys.databases
    WHERE
        is_cdc_enabled = 1 AND
        name = 'engagedb'
)
BEGIN
    EXEC sys.sp_cdc_enable_db;
END
