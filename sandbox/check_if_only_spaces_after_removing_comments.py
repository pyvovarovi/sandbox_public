import re

def check_if_only_spaces_after_removing_comments(text):
    # Regular expression to detect SQL comments
    comments_pattern = r"(--.*?$|/\*.*?\*/)"

    # Remove SQL comments from the text
    cleaned_text = re.sub(comments_pattern, '', text, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)

    # Check if the remaining text consists only of spaces or is empty
    return cleaned_text.strip() == ''

# Example texts
examples = [
    "SELECT * FROM users WHERE id = 100; -- Check user ID",
    "-- This is a comment about the next operations",
    "This is some text. -- SQL comment",
    "/* Start of SQL block */ SELECT name FROM employees; /* End of block */",
    "Just some plain old text without SQL."
]

# Testing the function on each example
results = [check_if_only_spaces_after_removing_comments(text) for text in examples]

# Display the results
results
