# External imports
import tkinter as tk
from tkinter import ttk

# Internal imports
from gui.create_project_window import CreateProjectWindow
from gui.archive_project_window import ArchiveProjectWindow
from gui.settings_window import settings_window
from utils.GUI_style import setup_style

class Main_window(ttk.Frame):
    def __init__(self, master):
        self.master = master
        ttk.Frame.__init__(self, self.master)
        setup_style()
        self.configure_gui()
        self.create_widgets()
   
    def configure_gui(self):
        # Create the main application window
        self.master.title("Project Management Software") # type: ignore
        self.master.geometry("200x200")  # type: ignore
    
    def create_widgets(self):
        # Create New Project button
        create_project_button = ttk.Button(
            self.master, 
            text="Create New Project", 
            command=self._on_create_project)
        create_project_button.pack(pady=10)
        
        # Create archive project button
        archive_project_button = ttk.Button(
            self.master, 
            text="Archive Project", 
            command=self._on_archive_project)
        archive_project_button.pack(pady=10)

        # Create settings button
        settings_button = ttk.Button(
            self.master,
            text="Settings",
            command=self._on_settings)
        settings_button.pack(pady=10)    
    
    def _on_create_project(self):
        create_project_window = CreateProjectWindow(self.master)
        create_project_window.grab_set()

    def _on_archive_project(self):
        archive_project_window = ArchiveProjectWindow(self.master)
        archive_project_window.grab_set()

    def _on_settings(self):
        settings_window()