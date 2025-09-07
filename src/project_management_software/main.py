from gui.main_window import Main_window
import tkinter as tk

def main():
    root = tk.Tk()
    main_app =  Main_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()