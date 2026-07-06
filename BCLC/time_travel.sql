-- =========================================================================================
-- Using the query_id 
SELECT * FROM DB.SCHEMA.TABLE_NAME BEFORE(STATEMENT => '<query_id_from_step_1>');
-- =========================================================================================
SELECT COUNT(*) FROM DB.SCHEMA.TABLE_NAME AT(OFFSET => -3600);   -- 1h ago
-- =========================================================================================
SELECT * FROM DB.SCHEMA.TABLE_NAME AT(TIMESTAMP => '2025-06-01 00:00:00'::TIMESTAMP_TZ);
-- =========================================================================================
UNDROP TABLE DB.SCHEMA.TABLE_NAME;
-- =========================================================================================
SELECT query_id, start_time, query_type, rows_produced, execution_status
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    END_TIME_RANGE_START => DATEADD('day', -7, CURRENT_TIMESTAMP()),
    END_TIME_RANGE_END   => CURRENT_TIMESTAMP()
))
WHERE query_text ILIKE '%TABLE_NAME%'
  AND query_type IN ('INSERT','UPDATE','DELETE','MERGE','TRUNCATE_TABLE','CREATE_TABLE_AS_SELECT')
ORDER BY start_time DESC;
-- =========================================================================================
SELECT query_id, start_time, query_type, rows_produced
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    DATEADD('day', -7, CURRENT_TIMESTAMP()),
    CURRENT_TIMESTAMP()
))
WHERE query_text ILIKE '%TABLE_NAME%'
ORDER BY start_time DESC;
-- =========================================================================================
-- use ACCOUNT_USAGE (no database context needed, up to 365 days):
SELECT query_id, start_time, query_type, rows_produced
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_text ILIKE '%TABLE_NAME%'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
-- =========================================================================================
