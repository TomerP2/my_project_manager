# External imports
import tkinter as tk

# Internal imports
from create_project_window import create_project_window

def main_window():
    # Create the main application window
    root = tk.Tk()
    root.title("Project Management Software")
    root.geometry("200x200")  # Set window size to provide more buffer around the button

    # Create New Project button
    create_project_button = tk.Button(root, text="Create New Project", command=create_project_window)
    create_project_button.pack(pady=20)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main_window()