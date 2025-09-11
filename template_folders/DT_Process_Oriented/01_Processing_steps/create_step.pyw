import os
import sys
import shutil
import re
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
from dotenv import dotenv_values

env_vars = dotenv_values()

def create_processing_step(step_name: str):
    # Set working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    # Exit if user cancels
    if not step_name:
        print("Operation cancelled")
        return

    # Clean up step name if it contains '='
    if '=' in step_name:
        step_name = step_name.split('=')[1].strip('"')

    # Define paths
    template_path = r'.\template_processing_step'
    current_dir = os.getcwd()

    # Find highest step number
    existing_steps = [d for d in os.listdir(current_dir) if os.path.isdir(d) and re.match(r'^\d{2}_', d)]
    next_number = 0 if not existing_steps else int(max(existing_steps)[0:2]) + 1

    # Create new folder name
    new_folder_name = f"{next_number:02d}_{step_name}"
    new_folder_path = os.path.join(current_dir, new_folder_name)

    # Copy template folder to new location
    shutil.copytree(template_path, new_folder_path)

    # Walk through the new folder and replace PROCESSING_STEP_NAME
    for root, dirs, files in os.walk(new_folder_path):
        # Rename directories containing PROCESSING_STEP_NAME
        for dir_name in dirs:
            if 'PROCESSING_STEP_NAME' in dir_name:
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, dir_name.replace('PROCESSING_STEP_NAME', step_name))
                os.rename(old_path, new_path)
        
        # Rename files and replace content
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Rename file if needed
            if 'PROCESSING_STEP_NAME' in file_name:
                new_file_path = os.path.join(root, file_name.replace('PROCESSING_STEP_NAME', step_name))
                os.rename(file_path, new_file_path)
                file_path = new_file_path
            
            # Replace content in files
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                if 'PROCESSING_STEP_NAME' in content:
                    content = content.replace('PROCESSING_STEP_NAME', step_name)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

                if 'CURRENT_DATE' in content:
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    content = content.replace('CURRENT_DATE', current_date)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

            except UnicodeDecodeError:
                # Skip binary files
                continue

    print(f"Created new processing step: {new_folder_name}")

if __name__ == "__main__":
    # If script was called with an argument, use it as step name
    try:
        step_name = sys.argv[1]
        
    # Else, show input dialog
    except IndexError: 
        # Create root window and hide it
        root = tk.Tk()
        root.withdraw()
        step_name = str(simpledialog.askstring("New Processing Step", "Enter the name of the new processing step:"))
    
    create_processing_step(step_name)
