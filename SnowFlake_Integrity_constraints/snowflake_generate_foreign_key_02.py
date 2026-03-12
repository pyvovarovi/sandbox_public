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

# Generate SQL queries to check for orphans and DDL statements for foreign keys
orphan_check_statements = []
ddl_statements = []

for fact_table in fact_tables:
    fact_columns = get_columns(fact_table)
    for dim_table in dimension_tables:
        dim_columns = get_columns(dim_table)
        common_fields = set(fact_columns) & set(dim_columns)
        for field in common_fields:
            # Orphan check query
            orphan_check_query = (
                f"SELECT {fact_table}.* FROM {fact_table} "
                f"LEFT JOIN {dim_table} ON {fact_table}.{field} = {dim_table}.{field} "
                f"WHERE {dim_table}.{field} IS NULL;"
            )
            orphan_check_statements.append(orphan_check_query)

            # Foreign key DDL statement
            fk_constraint_name = f"fk_{fact_table}_{field}"
            ddl_statement_fk = (
                f"ALTER TABLE {fact_table} ADD CONSTRAINT {fk_constraint_name} "
                f"FOREIGN KEY ({field}) REFERENCES {dim_table}({field});"
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
