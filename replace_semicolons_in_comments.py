import re

def replace_semicolons_in_comments(sql):
    # Function to replace semicolon with colon in a comment
    def replace_in_comment(match):
        comment = match.group(0)
        return comment.replace(';', ':')
    
    # Regex to find SQL comments (both single line and multi-line)
    comment_pattern = r'(--[^\n]*|/\*[\s\S]*?\*/)'
    
    # Replace semicolons in comments
    return re.sub(comment_pattern, replace_in_comment, sql)

# Example usage
sql_statement = """SELECT * FROM users; -- Select all users;
/* This is a multi-line comment;
It should also handle semicolons; */
INSERT INTO logs VALUES ('test', 'test'); -- Insert log;
"""
print(replace_semicolons_in_comments(sql_statement))
