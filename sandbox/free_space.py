import os
import shutil

def get_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    return total, used, free

def format_size(size):
    # Convert bytes to a more human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def print_disk_usage(path):
    total, used, free = get_disk_usage(path)
    print(f"Disk usage for path: {path}")
    print(f"Total: {format_size(total)}")
    print(f"Used: {format_size(used)}")
    print(f"Free: {format_size(free)}\n")

if __name__ == "__main__":
    # Check free space on the root file system
    root_path = '/'
    print_disk_usage(root_path)

    # Check free space for a specific path
    specific_path = '/path/to/your/directory'
    print_disk_usage(specific_path)
