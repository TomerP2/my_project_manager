# External imports
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import json
import os

# Internal imports
from create_project import create_project

def create_project_window():
    def browse_directory(entry, initial_dir=None):
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def on_create_project(directory_entry, project_name_entry, template_dir_entry, git_var):
        directory = directory_entry.get()
        project_name = project_name_entry.get()
        template_dir = template_dir_entry.get()
        use_git = git_var.get()

        if not directory or not project_name or not template_dir:
            messagebox.showerror("Error", "Directory, project name, and template directory are required.")
            return

        project_path = Path(directory) / project_name

        try:
            create_project(project_path, Path(template_dir), use_git)
            messagebox.showinfo("Success", "Project created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    # Get settings from settings.json
    with open(r"./settings.json", "r") as f:
        settings = json.load(f)

    # Create the main application window
    root = tk.Tk()
    root.title("Project Management Software")

    # Directory input
    directory_label = tk.Label(root, text="Directory:")
    directory_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    directory_entry = tk.Entry(root, width=40)
    default_directory = settings["default projects folder"]
    directory_entry.insert(0, default_directory)  # Set default directory
    directory_entry.grid(row=0, column=1, padx=10, pady=5)
    directory_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(directory_entry))
    directory_browse.grid(row=0, column=2, padx=10, pady=5)

    # Project name input
    project_name_label = tk.Label(root, text="Project Name:")
    project_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    project_name_entry = tk.Entry(root, width=40)
    project_name_entry.grid(row=1, column=1, padx=10, pady=5)

    # Template directory input
    template_dir_label = tk.Label(root, text="Template Directory:")
    template_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    template_dir_entry = tk.Entry(root, width=40)
    default_template_dir = settings["default templates folder"]
    template_dir_entry.insert(0, default_template_dir)  # Set default directory to project base folder
    template_dir_entry.grid(row=2, column=1, padx=10, pady=5)
    template_dir_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(template_dir_entry, default_template_dir))
    template_dir_browse.grid(row=2, column=2, padx=10, pady=5)

    # Git initialization checkbox
    git_var = tk.BooleanVar()
    git_checkbox = tk.Checkbutton(root, text="Initialize Git Repository", variable=git_var)
    git_checkbox.grid(row=3, column=1, pady=10)

    # Create project button
    create_project_button = tk.Button(root, text="Create Project", command=lambda: on_create_project(directory_entry, project_name_entry, template_dir_entry, git_var))
    create_project_button.grid(row=4, column=1, pady=20)

    # Run the application
    root.mainloop()
    
if __name__ == "__main__":
    create_project_window()