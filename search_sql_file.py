import os
import re

def find_files_with_dev(root_folder):
    matches = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".sql"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove all SQL comments from the content before searching
                    cleaned_content = re.sub(r'(--[^\n]*|/\*[\s\S]*?\*/)', '', content, flags=re.IGNORECASE)
                    # Search for '_dev' in a case-insensitive manner
                    if re.search(r'_dev', cleaned_content, re.IGNORECASE):
                        matches.append(file_path)
    return matches

# Example usage
root_folder = '/path/to/your/folder'
files = find_files_with_dev(root_folder)
for file in files:
    print(file)
