import os

OLD = "PROJECT_NAME"
NEW = "PROJECT_NAME"
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".vscode", ".obsidian"}  # add more if needed

def replace_in_file(path):
    """Replace occurrences of OLD with NEW in file contents."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if OLD in content:
            new_content = content.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
    except (UnicodeDecodeError, PermissionError):
        # Skip binary or unreadable files
        pass

def main():
    for root, dirs, files in os.walk(".", topdown=False):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        # Replace text inside files
        for filename in files:
            filepath = os.path.join(root, filename)
            replace_in_file(filepath)

            # Rename files if needed
            if OLD in filename:
                new_name = filename.replace(OLD, NEW)
                os.rename(filepath, os.path.join(root, new_name))

        # Rename directories if needed
        for dirname in dirs:
            if OLD in dirname:
                old_path = os.path.join(root, dirname)
                new_path = os.path.join(root, dirname.replace(OLD, NEW))
                os.rename(old_path, new_path)

if __name__ == "__main__":
    main()
