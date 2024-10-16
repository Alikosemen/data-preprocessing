import tkinter as tk
from gui import DatasetProcessorGUI

def main():
    root = tk.Tk()
    root.geometry("600x400")
    app = DatasetProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
