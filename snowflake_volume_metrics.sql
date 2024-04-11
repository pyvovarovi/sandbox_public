-- Set the variables
SET YourDatabaseName = 'YourDatabase'; -- Replace 'YourDatabase' with your actual database name
SET YourSchemaForMetrics = 'YourMetricsSchema'; -- Replace 'YourMetricsSchema' with your actual schema name for metrics
SET YourSchemaName = 'YourSchema'; -- Replace 'YourSchema' with the actual schema name you're querying

-- Use the variables in the query
SELECT 
    CONCAT($YourDatabaseName, '.', T.TABLE_SCHEMA, '.', T.TABLE_NAME) AS FULLY_QUALIFIED_TABLE_NAME, 
    T.TABLE_TYPE, 
    T.ROW_COUNT, 
    CASE
        WHEN M.BYTES < 1024 THEN CONCAT(M.BYTES, ' B')
        WHEN M.BYTES < 1024 * 1024 THEN CONCAT(ROUND(M.BYTES / 1024, 2), ' KB')
        WHEN M.BYTES < 1024 * 1024 * 1024 THEN CONCAT(ROUND(M.BYTES / (1024 * 1024), 2), ' MB')
        ELSE CONCAT(ROUND(M.BYTES / (1024 * 1024 * 1024), 2), ' GB')
    END AS SIZE_HUMAN_FORMAT,
    (
        SELECT COUNT(DISTINCT PARTITION_ORDINAL) 
        FROM IDENTIFIER($YourDatabaseName || '.' || $YourSchemaForMetrics || '.TABLE_STORAGE_METRICS') 
        WHERE TABLE_ID = T.TABLE_ID
    ) AS PARTITION_COUNT
FROM 
    IDENTIFIER($YourDatabaseName || '.INFORMATION_SCHEMA.TABLES') T
LEFT JOIN 
    IDENTIFIER($YourDatabaseName || '.' || $YourSchemaForMetrics || '.TABLE_STORAGE_METRICS') M 
    ON T.TABLE_CATALOG = M.TABLE_CATALOG 
    AND T.TABLE_SCHEMA = M.TABLE_SCHEMA 
    AND T.TABLE_NAME = M.TABLE_NAME
WHERE 
    T.TABLE_SCHEMA = $YourSchemaName
    AND T.TABLE_CATALOG = $YourDatabaseName
ORDER BY 
    T.TABLE_NAME;
