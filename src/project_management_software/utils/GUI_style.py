import tkinter as tk
from tkinter import ttk

def setup_style():
    print ("Setting up GUI style...")
    style = ttk.Style()

    # Pick a theme (built-in ones: "clam", "alt", "default", "classic")
    style.theme_use("clam")

    # Standardize buttons
    style.configure('TButton', font = 
               ('calibri', 10),
                foreground = 'black', padding=6)

    # Standardize labels
    style.configure("TLabel", font=("calibri", 10))

    # Standardize entries
    style.configure("TEntry", font=("calibri", 10))

    # Checkbox styling
    style.configure("TCheckbutton", font=("calibri", 10))
