# External imports
import shutil
import os
from pathlib import Path
import sys
import subprocess
import json

# Internal imports
try:
    import config
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import config

def create_project(project_path: Path, 
                   template_dirs: list[Path], 
                   use_git=False) -> None:        
    if not project_path:
        raise ValueError("Project path cannot be empty.")

    # Set working directory to the script's directory or PyInstaller temp folder
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)  # type: ignore
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # === Copy template folders ===
    if project_path.exists():
        raise FileExistsError(f"Project directory '{project_path}' already exists.")

    for template_dir in template_dirs:
        if not template_dir.exists():
            raise FileNotFoundError(f"Template directory '{template_dir}' not found.")
        shutil.copytree(template_dir, project_path, dirs_exist_ok=True)
    
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
            
    # === Replace 'PLACEHOLDER' in all files ===
    for file in project_path.rglob("*"):
        if file.is_file():
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content.replace("PLACEHOLDER", project_path.name)
                with open(file, "w", encoding="utf-8") as f:
                    f.write(content)
            except UnicodeDecodeError:
                # Skip binary files
                continue
            
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
            raise RuntimeError(f"Git initialization failed: {e}. Make sure git is installed and added to PATH.")