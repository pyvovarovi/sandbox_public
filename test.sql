CREATE TABLE dim_customer (
    dim_customer_id INT AUTOINCREMENT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(50),
    customer_address VARCHAR(100),
    effective_date DATE,
    expiration_date DATE,
    is_current VARCHAR(1)
);
-- ==============================================================================
CREATE TEMPORARY TABLE staging_customer (
    customer_id INT,
    customer_name VARCHAR(50),
    customer_address VARCHAR(100)
);
-- ==============================================================================
INSERT INTO staging_customer (customer_id, customer_name, customer_address)
VALUES 
(1, 'John Doe', '123 Main St'),
(2, 'Jane Smith', '456 Elm St');
-- ==============================================================================
MERGE INTO dim_customer AS target
USING (
    SELECT 
        s.customer_id, 
        s.customer_name, 
        s.customer_address,
        CURRENT_DATE() AS effective_date
    FROM staging_customer s
) AS source
ON target.customer_id = source.customer_id AND target.is_current = 'Y'
WHEN MATCHED THEN UPDATE SET 
    target.expiration_date = CURRENT_DATE(),
    target.is_current = 'N'
WHEN NOT MATCHED THEN INSERT 
    (customer_id, customer_name, customer_address, effective_date, is_current)
VALUES 
    (source.customer_id, source.customer_name, source.customer_address, source.effective_date, 'Y');
-- ==============================================================================
