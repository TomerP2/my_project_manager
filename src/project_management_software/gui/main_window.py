# External imports
import tkinter as tk

# Internal imports
from gui.create_project_window import create_project_window
from gui.archive_project_window import archive_project_window
from gui.settings_window import settings_window

def main_window():
    # Create the main application window
    root = tk.Tk()
    root.title("Project Management Software")
    root.geometry("200x200")  # Set window size to provide more buffer around the button

    # Create New Project button
    create_project_button = tk.Button(root, text="Create New Project", command=create_project_window)
    create_project_button.pack(pady=10)
    
    # Create archive project button
    archive_project_button = tk.Button(root, text="Archive Project", command=archive_project_window)
    archive_project_button.pack(pady=10)

    # Create settings button
    settings_button = tk.Button(root, text="Settings", command=settings_window)
    settings_button.pack(pady=10)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main_window()