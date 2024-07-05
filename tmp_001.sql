SELECT 
    c.table_name, 
    c.column_name 
FROM 
    information_schema.table_constraints tc
JOIN 
    information_schema.key_column_usage c 
    ON c.table_name = tc.table_name
    AND c.table_schema = tc.table_schema
    AND c.table_catalog = tc.table_catalog
    AND c.constraint_name = tc.constraint_name
WHERE 
    tc.constraint_type = 'PRIMARY KEY'
ORDER BY 
    c.table_name, 
    c.ordinal_position;
