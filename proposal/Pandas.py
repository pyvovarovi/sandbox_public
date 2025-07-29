import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "name": ["Manager", "Engineer"],
    "NAME": ["Full-Time", "Part-Time"],
    "NaMe": ["Team A", "Team B"],
    "Age": [25, 30]
})

def rename_case_insensitive_duplicates(df):
    lower_map = {}
    new_columns = []

    for col in df.columns:
        col_lower = col.lower()
        if col_lower in lower_map:
            lower_map[col_lower] += 1
            new_columns.append(f"{col}_{lower_map[col_lower]}")
        else:
            lower_map[col_lower] = 0
            new_columns.append(col)
    
    df.columns = new_columns
    return df

df = rename_case_insensitive_duplicates(df)
print(df)
