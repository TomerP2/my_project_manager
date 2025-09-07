import shutil
import os
from pathlib import Path
import sys
import subprocess
import json

def create_project(project_path: Path, 
                   template_dir: Path, 
                   use_git=False, 
                   create_obsidian_vault=False) -> None:
    # Get settings from settings.json
    with open(r"./Code/settings.json", "r") as f:
        settings = json.load(f)
        
    if not project_path:
        raise ValueError("Project path cannot be empty.")

    # Set working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    # === Copy template folder ===
    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory '{template_dir}' not found.")
    if project_path.exists():
        raise FileExistsError(f"Project directory '{project_path}' already exists.")

    shutil.copytree(template_dir, project_path)
    
    # === Create Obsidian vault if needed ===
    if create_obsidian_vault:
        obsidian_template = Path(settings["Obsidian vault template"])
        if not obsidian_template.exists():
            raise FileNotFoundError(f"Obsidian template directory '{obsidian_template}' not found.")
        
        shutil.copytree(obsidian_template, project_path, dirs_exist_ok=True)

    # === Rename folders containing 'PLACEHOLDER' (deepest first) ===
    for folder in sorted(project_path.rglob("*"), key=lambda p: -p.relative_to(project_path).parts.__len__()):
        if folder.is_dir() and "PLACEHOLDER" in folder.name:
            new_name = folder.name.replace("PLACEHOLDER", project_path.name)
            folder.rename(folder.with_name(new_name))

    # === Rename files containing 'PLACEHOLDER' ===
    for file in project_path.rglob("*"):
        if file.is_file() and "PLACEHOLDER" in file.name:
            new_name = file.name.replace("PLACEHOLDER", project_path.name)
            file.rename(file.with_name(new_name))
            
    # === Replace 'PROJECT_PATH_PLACEHOLDER' in .env file ===
    env_example_path = project_path / ".env"
    if env_example_path.exists():
        with open(env_example_path, "r") as file:
            content = file.read()
        content = content.replace("PROJECT_PATH_PLACEHOLDER", str(project_path.resolve()).replace("\\", "/"))
        with open(env_example_path, "w") as file:
            file.write(content)
                    
    # === Create a new git repository in project directory ===
    if use_git:    
        try:
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True)
        except Exception as e:
            print(f"Warning: Git initialization failed. {e}")