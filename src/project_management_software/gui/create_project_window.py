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

    # Ensure 'settings' is loaded at the beginning of the function
    with open(r"./Code/settings.json", "r") as f:
        settings = json.load(f)

    # Ensure 'root' is defined before any UI elements are created
    root = tk.Tk()
    root.title("Project Management Software")

    # Template directory input
    template_dir_label = tk.Label(root, text="Template Directory:")
    template_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    # Get default template directory from settings
    default_template_dir = settings["default templates folder"]

    # Create a list of template folders from the template directory
    try:
        template_folders = [folder.name for folder in Path(default_template_dir).iterdir() if folder.is_dir()]
    except FileNotFoundError:
        template_folders = []

    # Dropdown menu for selecting a template
    selected_template = tk.StringVar()
    if template_folders:
        selected_template.set(template_folders[0])  # Set default selection to the first template
    template_dropdown = tk.OptionMenu(root, selected_template, *template_folders)
    template_dropdown.grid(row=2, column=1, padx=10, pady=5)

    # Button to refresh the template list
    def refresh_template_list():
        try:
            updated_folders = [folder.name for folder in Path(default_template_dir).iterdir() if folder.is_dir()]
            menu = template_dropdown["menu"]
            menu.delete(0, "end")
            for folder in updated_folders:
                menu.add_command(label=folder, command=lambda value=folder: selected_template.set(value))
            if updated_folders:
                selected_template.set(updated_folders[0])
        except FileNotFoundError:
            messagebox.showerror("Error", "Template directory not found.")

    refresh_button = tk.Button(root, text="Refresh", command=refresh_template_list)
    refresh_button.grid(row=2, column=2, padx=10, pady=5)

    def on_create_project(directory_entry, project_name_entry, git_var, use_obsidian_var):
        directory = directory_entry.get()
        project_name = project_name_entry.get()
        chosen_template = selected_template.get()
        use_git = git_var.get()
        use_obsidian = use_obsidian_var.get()

        if not directory or not project_name or not chosen_template:
            messagebox.showerror("Error", "Directory, project name, and template selection are required.")
            return

        project_path = Path(directory) / project_name
        template_path = Path(default_template_dir) / chosen_template

        try:
            create_project(project_path, template_path, use_git, use_obsidian)
            messagebox.showinfo("Success", "Project created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            

    # Directory input
    directory_label = tk.Label(root, text="Directory:")
    directory_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    directory_entry = tk.Entry(root, width=40)
    default_directory = settings["default projects folder"]
    directory_entry.insert(0, default_directory)  # Set default directory
    directory_entry.grid(row=0, column=1, padx=10, pady=5)
    directory_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(directory_entry, default_directory))
    directory_browse.grid(row=0, column=2, padx=10, pady=5)

    # Project name input
    project_name_label = tk.Label(root, text="Project Name:")
    project_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    project_name_entry = tk.Entry(root, width=40)
    project_name_entry.grid(row=1, column=1, padx=10, pady=5)

    # Git initialization checkbox
    git_var = tk.BooleanVar()
    git_checkbox = tk.Checkbutton(root, text="Initialize Git Repository", variable=git_var)
    git_checkbox.grid(row=3, column=1, pady=10)
    
    # Obsidian vault checkbox
    use_obsidian_var = tk.BooleanVar()
    git_checkbox = tk.Checkbutton(root, text="Create Obsidian Vault", variable=use_obsidian_var)
    git_checkbox.grid(row=4, column=1, pady=10)

    # Create project button
    create_project_button = tk.Button(root, text="Create Project", command=lambda: on_create_project(directory_entry, project_name_entry, git_var, use_obsidian_var))
    create_project_button.grid(row=5, column=1, pady=20)

    # Run the application
    root.mainloop()
    
if __name__ == "__main__":
    create_project_window()