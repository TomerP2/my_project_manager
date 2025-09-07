from tkinter import Tk, Label, Button, filedialog
from pathlib import Path
from core.archive_project import archive_project

def archive_project_window():
    """
    Creates a GUI that calls archive_project from archive_project.py with given user inputs.
    """
    def select_project_folder():
        folder = filedialog.askdirectory(title="Select Project Folder")
        if folder:
            project_folder_label.config(text=folder)

    def select_archive_folder():
        folder = filedialog.askdirectory(title="Select Archive Folder")
        if folder:
            archive_folder_label.config(text=folder)

    def archive():
        project_path = Path(project_folder_label.cget("text"))
        archive_path = Path(archive_folder_label.cget("text"))
        try:
            archive_project(project_path, archive_path)
            status_label.config(text="Project archived successfully!", fg="green")
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")

    # Initialize the GUI window
    root = Tk()
    root.title("Archive Project")

    # Project folder selection
    Label(root, text="Project Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    project_folder_label = Label(root, text="", width=50, anchor="w")
    project_folder_label.grid(row=0, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=select_project_folder).grid(row=0, column=2, padx=10, pady=5)

    # Archive folder selection
    Label(root, text="Archive Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    archive_folder_label = Label(root, text="", width=50, anchor="w")
    archive_folder_label.grid(row=1, column=1, padx=10, pady=5)
    Button(root, text="Browse", command=select_archive_folder).grid(row=1, column=2, padx=10, pady=5)

    # Archive button
    Button(root, text="Archive", command=archive).grid(row=2, column=1, pady=10)

    # Status label
    status_label = Label(root, text="", fg="blue")
    status_label.grid(row=3, column=0, columnspan=3, pady=10)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    archive_project_window()