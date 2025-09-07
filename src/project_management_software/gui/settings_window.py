import json
import tkinter as tk
from tkinter import ttk, messagebox

def settings_window():
    # Load settings from the JSON file
    settings_file = "./settings.json"
    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Settings file '{settings_file}' not found.")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Settings file '{settings_file}' is not a valid JSON file.")
        return

    # Create the main window
    root = tk.Tk()
    root.title("Settings")

    # Create a frame for the settings
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky="nsew")

    # Create input fields dynamically based on the keys in the JSON file
    entries = {}
    for idx, (key, value) in enumerate(settings.items()):
        ttk.Label(frame, text=key).grid(row=idx, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.insert(0, value)
        entry.grid(row=idx, column=1, pady=5)
        entries[key] = entry

    # Save settings back to the JSON file
    def save_settings():
        for key, entry in entries.items():
            settings[key] = entry.get()
        try:
            with open(settings_file, "w") as file:
                json.dump(settings, file, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    # Add Save and Cancel buttons
    ttk.Button(frame, text="Save", command=save_settings).grid(row=len(settings), column=0, pady=10)
    ttk.Button(frame, text="Cancel", command=root.destroy).grid(row=len(settings), column=1, pady=10)

    # Run the application
    root.mainloop()
    
if __name__ == "__main__":
    settings_window()