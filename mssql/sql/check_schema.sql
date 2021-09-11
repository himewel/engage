SET NOCOUNT ON;

SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE
    TABLE_SCHEMA = 'db' AND
    TABLE_NAME = 'users';
