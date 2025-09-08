# External imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json
import os

# Internal imports
from core.create_project import create_project

class CreateProjectWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("500x300")
        self.title("Create Project")

        self.settings = self._load_settings()
        self.default_template_dir = self.settings["default templates folder"]
        self.default_directory = self.settings["default projects folder"]

        self.selected_template = tk.StringVar()
        self.git_var = tk.BooleanVar()
        self.use_obsidian_var = tk.BooleanVar()

        self._create_widgets()

    def _load_settings(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(r"../settings.json", "r") as f:
            return json.load(f)

    def _browse_directory(self, entry, initial_dir=None):
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def _refresh_template_list(self):
        try:
            updated_folders = [folder.name for folder in Path(self.default_template_dir).iterdir() if folder.is_dir()]
            menu = self.template_dropdown["menu"]
            menu.delete(0, "end")
            for folder in updated_folders:
                menu.add_command(label=folder, command=lambda value=folder: self.selected_template.set(value))
            if updated_folders:
                self.selected_template.set(updated_folders[0])
        except FileNotFoundError:
            messagebox.showerror("Error", "Template directory not found.")

    def _on_create_project(self):
        directory = self.directory_entry.get()
        project_name = self.project_name_entry.get()
        chosen_template = self.selected_template.get()
        use_git = self.git_var.get()
        use_obsidian = self.use_obsidian_var.get()

        if not directory or not project_name or not chosen_template:
            messagebox.showerror("Error", "Directory, project name, and template selection are required.")
            return

        project_path = Path(directory) / project_name
        template_path = Path(self.default_template_dir) / chosen_template

        try:
            create_project(project_path, template_path, use_git, use_obsidian)
            messagebox.showinfo("Success", "Project created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _create_widgets(self):
        # Directory input
        ttk.Label(self, text="Directory:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.directory_entry = ttk.Entry(self, width=40)
        self.directory_entry.insert(0, self.default_directory)
        self.directory_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(self, text="Browse", command=lambda: self._browse_directory(self.directory_entry, self.default_directory)).grid(row=0, column=2, padx=10, pady=5)

        # Project name input
        ttk.Label(self, text="Project Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.project_name_entry = ttk.Entry(self, width=40)
        self.project_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Template dropdown
        ttk.Label(self, text="Template Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        try:
            template_folders = [folder.name for folder in Path(self.default_template_dir).iterdir() if folder.is_dir()]
        except FileNotFoundError:
            template_folders = []

        if template_folders:
            self.selected_template.set(template_folders[0])
        self.template_dropdown = ttk.OptionMenu(self, self.selected_template, *template_folders)
        self.template_dropdown.grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self, text="Refresh", command=self._refresh_template_list).grid(row=2, column=2, padx=10, pady=5)

        # Git initialization checkbox
        ttk.Checkbutton(self, text="Initialize Git Repository", variable=self.git_var).grid(row=3, column=1, pady=10)

        # Obsidian vault checkbox
        ttk.Checkbutton(self, text="Create Obsidian Vault", variable=self.use_obsidian_var).grid(row=4, column=1, pady=10)

        # Create project button
        ttk.Button(self, text="Create Project", command=self._on_create_project).grid(row=5, column=1, pady=20)