IF NOT EXISTS (
    SELECT *
    FROM sys.schemas
    WHERE name = 'db'
)
EXEC('CREATE SCHEMA db');

-- USERS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'users'
)
    BEGIN
        CREATE TABLE db.users (
            userId        INTEGER,
            image         VARCHAR(300)
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE db.users;
    END

-- ROUNDS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'rounds'
)
BEGIN
        CREATE TABLE db.rounds (
            roundId               INTEGER,
            name                  VARCHAR(300),
            roundscorebonus       INTEGER,
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE db.rounds;
    END

-- ACTIVITIES
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'activities'
)
    BEGIN
        CREATE TABLE db.activities (
            activityid      INTEGER,
            roundid         INTEGER,
            activityweight  FLOAT
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE db.activities;
    END

-- ANSWERS
IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'answers'
)
    BEGIN
        CREATE TABLE db.answers (
            activityid          INTEGER,
            userid              INTEGER,
            scoreofaccuracy     FLOAT,
            answerdatetime      DATETIME,
            approved            VARCHAR(5)
        );
    END
ELSE
    BEGIN
        TRUNCATE TABLE db.users;
    END
