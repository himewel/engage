IF NOT EXISTS (
    SELECT *
    FROM sys.schemas
    WHERE name = 'db'
)
EXEC('CREATE SCHEMA db');

IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'users'
)
CREATE TABLE db.users (
    userId        INTEGER,
    userStatus    VARCHAR(5),
    maxScore      INTEGER,
    score         FLOAT,
    image         VARCHAR(300),
    position      INTEGER,
    myRanking     VARCHAR(5)
);

IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'rounds'
)
CREATE TABLE db.rounds (
    roundId               INTEGER,
    userId                INTEGER,
    name                  VARCHAR(300),
    status                VARCHAR(15),
    roundscorebonus       INTEGER,
    lastattemptstatus     VARCHAR(25),
    approved              INTEGER,
    waiting               VARCHAR(5),
    answerdate            DATE,
    showstars             VARCHAR(5),
    showscore             VARCHAR(5),
    stars                 INTEGER
);

IF NOT EXISTS (
    SELECT * FROM sys.tables t
    JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE
        s.name = 'db' AND
        t.name = 'rounds'
)
CREATE TABLE db.rounds (
    roundId               INTEGER,
    userId                INTEGER,
    name                  VARCHAR(300),
    status                VARCHAR(15),
    roundscorebonus       INTEGER,
    lastattemptstatus     VARCHAR(25),
    approved              INTEGER,
    waiting               VARCHAR(5),
    answerdate            DATE,
    showstars             VARCHAR(5),
    showscore             VARCHAR(5),
    stars                 INTEGER
);
