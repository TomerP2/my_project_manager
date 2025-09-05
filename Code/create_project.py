import shutil
import os
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
from dotenv import dotenv_values

env_vars = dotenv_values()

def create_project():
    project_name = entry.get().strip()
    
    if not project_name:
        messagebox.showerror("Error", "Please enter a project name")
        return

    # Set working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    template_dir = Path(env_vars["TEMPLATE_PROJECT_FOLDER_PATH"])
    projects_dir = Path(env_vars["PROJECTS_FOLDER"]) 
    new_dir = projects_dir / project_name 

    # === Ensure Projects directory exists ===
    if not projects_dir.exists():
        projects_dir.mkdir(parents=True)

    # === Copy template folder ===
    if not template_dir.exists():
        messagebox.showerror("Error", f"Template directory '{template_dir}' not found.")
        return

    if new_dir.exists():
        messagebox.showerror("Error", f"Target directory '{new_dir}' already exists.")
        return

    shutil.copytree(template_dir, new_dir)

    # === Rename folders containing 'PLACEHOLDER' (deepest first) ===
    for folder in sorted(new_dir.rglob("*"), key=lambda p: -p.relative_to(new_dir).parts.__len__()):
        if folder.is_dir() and "PLACEHOLDER" in folder.name:
            new_name = folder.name.replace("PLACEHOLDER", project_name)
            folder.rename(folder.with_name(new_name))

    # === Rename files containing 'PLACEHOLDER' ===
    for file in new_dir.rglob("*"):
        if file.is_file() and "PLACEHOLDER" in file.name:
            new_name = file.name.replace("PLACEHOLDER", project_name)
            file.rename(file.with_name(new_name))
            
    # === Replace 'PROJECT_PATH_PLACEHOLDER' in .env file ===
    env_example_path = new_dir / ".env"
    if env_example_path.exists():
        with open(env_example_path, "r") as file:
            content = file.read()
        content = content.replace("PROJECT_PATH_PLACEHOLDER", str(new_dir.resolve()).replace("\\", "/"))
        with open(env_example_path, "w") as file:
            file.write(content)
                    
    # === Create a new git repository in project directory ===
    try:
        subprocess.run(["git", "init"], cwd=new_dir, check=True)
        subprocess.run(["git", "add", "."], cwd=new_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=new_dir, check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize Git repository: {e}")
        return
    
    messagebox.showinfo("Success", f"Project folder created: {new_dir}")
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Create Project")
root.geometry("400x150")

# Create and pack widgets
label = tk.Label(root, text="Enter Project Name:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=10)

create_button = tk.Button(root, text="Create Project", command=create_project, font=("Arial", 11))
create_button.pack(pady=10)

# Center the window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.mainloop()
