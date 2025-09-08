import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from core.archive_project import archive_project

class ArchiveProjectWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('500x200')
        self.title('Archive Project')

        self.project_folder_label = ttk.Label(self, text="", width=50, anchor="w")
        self.archive_folder_label = ttk.Label(self, text="", width=50, anchor="w")
        self.status_label = ttk.Label(self, text="", foreground="blue")

        self._create_widgets()

    def _select_project_folder(self):
        folder = filedialog.askdirectory(title="Select Project Folder")
        if folder:
            self.project_folder_label.config(text=folder)

    def _select_archive_folder(self):
        folder = filedialog.askdirectory(title="Select Archive Folder")
        if folder:
            self.archive_folder_label.config(text=folder)

    def _archive(self):
        project_path = Path(self.project_folder_label.cget("text"))
        archive_path = Path(self.archive_folder_label.cget("text"))
        try:
            archive_project(project_path, archive_path)
            self.status_label.config(text="Project archived successfully!", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", foreground="red")
            
    def _create_widgets(self):
        # Project folder selection
        ttk.Label(self, text="Project Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.project_folder_label.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(self, text="Browse", command=self._select_project_folder).grid(row=0, column=2, padx=10, pady=5)

        # Archive folder selection
        ttk.Label(self, text="Archive Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.archive_folder_label.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self, text="Browse", command=self._select_archive_folder).grid(row=1, column=2, padx=10, pady=5)

        # Archive button
        ttk.Button(self, text="Archive", command=self._archive).grid(row=2, column=1, pady=10)

        # Status label
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)
