import os
import shutil

# Define the folders to replace and ignore
folders_to_replace = ['./.obsidian']
folders_to_ignore = ['./.git']

def should_ignore(path, ignore_list):
    return any(os.path.commonpath([path, ignore]) == ignore for ignore in ignore_list)

def sync_folders(template_root, project_root):
    for root, dirs, files in os.walk(template_root):
        rel_path = os.path.relpath(root, template_root)
        target_root = os.path.join(project_root, rel_path)

        # Skip ignored folders
        if should_ignore(rel_path, folders_to_ignore):
            continue

        # Ensure the directory exists in the project
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            template_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_root, file)

            # Determine if this file should be replaced
            if should_ignore(rel_path, folders_to_replace):
                # Replace the file
                shutil.copy2(template_file_path, target_file_path)
            elif not os.path.exists(target_file_path):
                # Only copy if it doesn't exist
                shutil.copy2(template_file_path, target_file_path)

        # Ensure empty directories are created
        for dir in dirs:
            dir_path = os.path.join(target_root, dir)
            os.makedirs(dir_path, exist_ok=True)

def get_project_folders(projects_root):
    """Get all immediate subdirectories in the projects root directory."""
    project_folders = []
    for item in os.listdir(projects_root):
        full_path = os.path.join(projects_root, item)
        if os.path.isdir(full_path) and item != 'template_project':
            project_folders.append(full_path)
    return project_folders

def main():
    # Get the current directory (assumed to be the projects root)
    projects_root = os.path.dirname(os.path.abspath(__file__))
    template_project = os.path.join(projects_root, 'template_project')
    
    # Verify template project exists
    if not os.path.exists(template_project):
        print(f"Error: Template project not found at {template_project}")
        return

    # Get all project folders
    project_folders = get_project_folders(projects_root)
    
    # Sync each project
    for project in project_folders:
        print(f"Syncing project: {os.path.basename(project)}")
        sync_folders(template_project, project)
        print(f"Completed sync for: {os.path.basename(project)}")

    print("All projects have been synchronized.")

if __name__ == "__main__":
    main()

