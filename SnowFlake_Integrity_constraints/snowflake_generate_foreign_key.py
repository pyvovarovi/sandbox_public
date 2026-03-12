
import snowflake.connector

# Define Snowflake connection parameters
conn_params = {
    'user': '<your_username>',
    'password': '<your_password>',
    'account': '<your_account>',
    'warehouse': '<your_warehouse>',
    'database': '<your_database>',
    'schema': '<your_schema>'
}

# Connect to Snowflake
conn = snowflake.connector.connect(**conn_params)
cur = conn.cursor()

# Query to get fact and dimension tables
fact_tables_query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '<your_schema>'
AND table_name LIKE 'fact_%';
"""

dimension_tables_query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '<your_schema>'
AND table_name LIKE 'dim_%';
"""

# Execute queries
cur.execute(fact_tables_query)
fact_tables = [row[0] for row in cur.fetchall()]

cur.execute(dimension_tables_query)
dimension_tables = [row[0] for row in cur.fetchall()]

# Function to get columns for a table
def get_columns(table_name):
    cur.execute(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = '<your_schema>'
    AND table_name = '{table_name}';
    """)
    return [row[0] for row in cur.fetchall()]

# Function to get composite keys for a table
def get_composite_keys(table_name):
    cur.execute(f"""
    SELECT kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    WHERE tc.table_schema = '<your_schema>'
    AND tc.table_name = '{table_name}'
    AND tc.constraint_type = 'FOREIGN KEY'
    ORDER BY kcu.ordinal_position;
    """)
    composite_keys = {}
    for row in cur.fetchall():
        key_name = row[0]
        composite_keys.setdefault(key_name, []).append(row[1])
    return composite_keys

# Generate SQL queries to check for orphans and DDL statements for foreign keys
orphan_check_statements = []
ddl_statements = []

for fact_table in fact_tables:
    fact_columns = get_columns(fact_table)
    for dim_table in dimension_tables:
        dim_columns = get_columns(dim_table)
        
        # Generate composite key pairs
        fact_composite_keys = get_composite_keys(fact_table)
        dim_composite_keys = get_composite_keys(dim_table)
        
        for key_name, fact_key_columns in fact_composite_keys.items():
            if key_name in dim_composite_keys:
                dim_key_columns = dim_composite_keys[key_name]
                if set(fact_key_columns) == set(dim_key_columns):
                    # Create composite key condition
                    join_condition = " AND ".join(
                        [f"{fact_table}.{col} = {dim_table}.{col}" for col in fact_key_columns]
                    )
                    check_condition = " AND ".join(
                        [f"{dim_table}.{col} IS NULL" for col in fact_key_columns]
                    )
                    orphan_check_query = (
                        f"SELECT {fact_table}.* FROM {fact_table} "
                        f"LEFT JOIN {dim_table} ON {join_condition} "
                        f"WHERE {check_condition};"
                    )
                    orphan_check_statements.append(orphan_check_query)
                    
                    fk_constraint_name = f"fk_{fact_table}_{dim_table}_{'_'.join(fact_key_columns)}"
                    ddl_statement_fk = (
                        f"ALTER TABLE {fact_table} ADD CONSTRAINT {fk_constraint_name} "
                        f"FOREIGN KEY ({', '.join(fact_key_columns)}) "
                        f"REFERENCES {dim_table}({', '.join(dim_key_columns)});"
                    )
                    ddl_statements.append(ddl_statement_fk)

# Close the cursor and connection
cur.close()
conn.close()

# Write SQL queries and DDL statements to a file
with open("check_orphans_and_foreign_keys_ddl.sql", "w") as file:
    file.write("-- SQL queries to check for orphan records\n")
    for query in orphan_check_statements:
        file.write(query + "\n")
    file.write("\n-- DDL statements to add foreign key constraints\n")
    for statement in ddl_statements:
        file.write(statement + "\n")

print("DDL file for checking orphans and adding foreign keys has been generated: check_orphans_and_foreign_keys_ddl.sql")
