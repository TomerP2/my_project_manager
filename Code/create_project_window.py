# External imports
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Internal imports
from create_project import create_project

def create_project_window():
    def browse_directory(entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

    def on_create_project(project_path_entry, template_dir_entry, git_var):
        project_path = project_path_entry.get()
        template_dir = template_dir_entry.get()
        use_git = git_var.get()

        if not project_path or not template_dir:
            messagebox.showerror("Error", "Both project path and template directory are required.")
            return

        try:
            create_project(Path(project_path), Path(template_dir), use_git)
            messagebox.showinfo("Success", "Project created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create the main application window
    root = tk.Tk()
    root.title("Project Management Software")

    # Project path input
    project_path_label = tk.Label(root, text="Project Directory:")
    project_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    project_path_entry = tk.Entry(root, width=40)
    project_path_entry.grid(row=0, column=1, padx=10, pady=5)
    project_path_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(project_path_entry))
    project_path_browse.grid(row=0, column=2, padx=10, pady=5)

    # Template directory input
    template_dir_label = tk.Label(root, text="Template Directory:")
    template_dir_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    template_dir_entry = tk.Entry(root, width=40)
    template_dir_entry.grid(row=1, column=1, padx=10, pady=5)
    template_dir_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(template_dir_entry))
    template_dir_browse.grid(row=1, column=2, padx=10, pady=5)

    # Git initialization checkbox
    git_var = tk.BooleanVar()
    git_checkbox = tk.Checkbutton(root, text="Initialize Git Repository", variable=git_var)
    git_checkbox.grid(row=2, column=1, pady=10)

    # Create project button
    create_project_button = tk.Button(root, text="Create Project", command=lambda: on_create_project(project_path_entry, template_dir_entry, git_var))
    create_project_button.grid(row=3, column=1, pady=20)

    # Run the application
    root.mainloop()
    
if __name__ == "__main__":
    create_project_window()