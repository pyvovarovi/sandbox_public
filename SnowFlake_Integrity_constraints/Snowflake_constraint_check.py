import snowflake.connector

# Establish connection to Snowflake
conn = snowflake.connector.connect(
    user='your_user',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema'
)

def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[1] for table in tables]

def get_table_ddl(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    ddl = cursor.fetchone()[0]
    return ddl

def generate_duplicate_check_scripts(table_ddl):
    import re
    scripts = []
    # Regex patterns to find primary keys and unique constraints
    pk_pattern = re.compile(r"PRIMARY KEY \((.*?)\)")
    unique_pattern = re.compile(r"UNIQUE \((.*?)\)")

    # Find all primary keys and unique constraints
    primary_keys = pk_pattern.findall(table_ddl)
    unique_constraints = unique_pattern.findall(table_ddl)

    # Generate scripts for primary keys
    for pk in primary_keys:
        columns = pk.split(',')
        columns = [col.strip() for col in columns]
        column_list = ', '.join(columns)
        script = f"SELECT {column_list}, COUNT(*) as cnt FROM {table_name} GROUP BY {column_list} HAVING cnt > 1;"
        scripts.append(script)

    # Generate scripts for unique constraints
    for unique in unique_constraints:
        columns = unique.split(',')
        columns = [col.strip() for col in columns]
        column_list = ', '.join(columns)
        script = f"SELECT {column_list}, COUNT(*) as cnt FROM {table_name} GROUP BY {column_list} HAVING cnt > 1;"
        scripts.append(script)

    return scripts

# Get all table names
tables = get_table_names(conn)

# Generate and print scripts for each table
for table in tables:
    ddl = get_table_ddl(conn, table)
    scripts = generate_duplicate_check_scripts(ddl)
    for script in scripts:
        print(script)

# Close the connection
conn.close()
