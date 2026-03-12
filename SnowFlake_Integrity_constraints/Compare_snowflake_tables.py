
import re

def read_ddl(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_ddl(ddl_content):
    tables = {}
    table_pattern = re.compile(r'CREATE TABLE (\w+)\s*\((.*?)\);', re.S)
    column_pattern = re.compile(r'(\w+)\s+([\w\(\)]+)', re.S)
    constraint_pattern = re.compile(r'CONSTRAINT (\w+) (.*?)\s*,', re.S)

    matches = table_pattern.findall(ddl_content)
    for match in matches:
        table_name, body = match
        columns = column_pattern.findall(body)
        constraints = constraint_pattern.findall(body)
        
        column_dict = {col[0]: col[1] for col in columns}
        constraint_dict = {con[0]: con[1].strip() for con in constraints}
        
        tables[table_name] = {'columns': column_dict, 'constraints': constraint_dict}

    return tables

def compare_tables(tables1, tables2):
    all_tables = set(tables1.keys()).union(set(tables2.keys()))
    differences = {}

    for table in all_tables:
        if table not in tables1:
            differences[table] = {'status': 'only in second DDL'}
        elif table not in tables2:
            differences[table] = {'status': 'only in first DDL'}
        else:
            table_diff = {}
            columns1 = tables1[table]['columns']
            columns2 = tables2[table]['columns']
            constraints1 = tables1[table]['constraints']
            constraints2 = tables2[table]['constraints']
            
            all_columns = set(columns1.keys()).union(set(columns2.keys()))
            all_constraints = set(constraints1.keys()).union(set(constraints2.keys()))
            
            column_differences = {}
            for column in all_columns:
                if column not in columns1:
                    column_differences[column] = {'status': 'only in second DDL'}
                elif column not in columns2:
                    column_differences[column] = {'status': 'only in first DDL'}
                elif columns1[column] != columns2[column]:
                    column_differences[column] = {
                        'first DDL': columns1[column],
                        'second DDL': columns2[column]
                    }

            constraint_differences = {}
            for constraint in all_constraints:
                if constraint not in constraints1:
                    constraint_differences[constraint] = {'status': 'only in second DDL'}
                elif constraint not in constraints2:
                    constraint_differences[constraint] = {'status': 'only in first DDL'}
                elif constraints1[constraint] != constraints2[constraint]:
                    constraint_differences[constraint] = {
                        'first DDL': constraints1[constraint],
                        'second DDL': constraints2[constraint]
                    }

            if column_differences:
                table_diff['columns'] = column_differences
            if constraint_differences:
                table_diff['constraints'] = constraint_differences

            if table_diff:
                differences[table] = table_diff

    return differences

# Example usage:
ddl1 = read_ddl('ddl1.sql')
ddl2 = read_ddl('ddl2.sql')

tables1 = parse_ddl(ddl1)
tables2 = parse_ddl(ddl2)

differences = compare_tables(tables1, tables2)

for table, diff in differences.items():
    print(f"Table: {table}")
    for category, details in diff.items():
        print(f"  {category.capitalize()}:")
        for name, info in details.items():
            print(f"    {name}: {info}")
