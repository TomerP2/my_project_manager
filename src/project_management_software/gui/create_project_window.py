# External imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json
import os
import sys

# Internal imports
try:
    from core.create_project import create_project
    import config
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from core.create_project import create_project
    import config


class CreateProjectWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("500x400")
        self.title("Create Project")

        self.settings = config.settings
        self.templates_dir = self.settings["default templates folder"]
        self.default_directory = self.settings["default projects folder"]

        self.selected_templates = []
        self.git_var = tk.BooleanVar()

        self._create_widgets()
        self._refresh_template_list()

    def _browse_directory(self, entry, initial_dir=None):
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def _refresh_template_list(self):
        try:
            updated_folders = [folder.name for folder in Path(self.templates_dir).iterdir() if folder.is_dir()]
            self.template_checklist.delete(0, tk.END)
            for folder in updated_folders:
                self.template_checklist.insert(tk.END, folder)
        except FileNotFoundError:
            messagebox.showerror("Error", "Template directory not found.")

    def _on_create_project(self):
        directory = self.directory_entry.get()
        project_name = self.project_name_entry.get()
        selected_indices = self.template_checklist.curselection()
        self.selected_templates = [Path(self.templates_dir) / self.template_checklist.get(i) for i in selected_indices]
        use_git = self.git_var.get()

        if not directory or not project_name or not self.selected_templates:
            messagebox.showerror("Error", "Directory, project name, and at least one template selection are required.")
            return

        project_path = Path(directory) / project_name

        try:
            create_project(project_path, self.selected_templates, use_git)
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

        # Template checklist
        ttk.Label(self, text="Templates:").grid(row=2, column=0, padx=10, pady=5, sticky="ne")
        self.template_checklist = tk.Listbox(self, selectmode=tk.MULTIPLE, height=10, width=40)
        self.template_checklist.grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self, text="Refresh", command=self._refresh_template_list).grid(row=2, column=2, padx=10, pady=5)

        # Git initialization checkbox
        ttk.Checkbutton(self, text="Initialize Git Repository", variable=self.git_var).grid(row=3, column=1, pady=10)

        # Create project button
        ttk.Button(self, text="Create Project", command=self._on_create_project).grid(row=4, column=1, pady=20)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    CreateProjectWindow(root)
    root.mainloop()