import tkinter as tk
from tkinter import messagebox
import os
import file_io
import encoding


class DatasetProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataset Processor")
        self.dataset_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        self.dataset_var.set("Select a dataset")
        self.target_var.set("Select a target variable")
        datasets = file_io.load_datasets()

        tk.Label(self.root, text="Select Dataset:").pack(pady=10)
        self.dataset_dropdown = tk.OptionMenu(self.root, self.dataset_var, *datasets, command=self.on_dataset_select)
        self.dataset_dropdown.pack(pady=5)

        tk.Label(self.root, text="Select Target Variable:").pack(pady=10)
        self.target_dropdown = tk.OptionMenu(self.root, self.target_var, ())
        self.target_dropdown.pack(pady=5)

        run_button = tk.Button(self.root, text="Run Program", command=self.run_program)
        run_button.pack(pady=20)

    def on_dataset_select(self, event):
        selected_file = self.dataset_var.get()
        if selected_file:
            try:
                headers, _ = file_io.read_dataset(selected_file)
                self.target_dropdown["menu"].delete(0, "end")
                for header in headers:
                    self.target_dropdown["menu"].add_command(label=header, command=tk._setit(self.target_var, header))
                self.target_var.set(headers[0])
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")

    def run_program(self):
        selected_file = self.dataset_var.get()
        target_variable = self.target_var.get()

        if not selected_file or not target_variable:
            messagebox.showerror("Error", "Please select a dataset and target variable.")
            return

        try:
            result = encoding.encode(selected_file, target_variable)
            self.show_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_result(self, result):
        result_window = tk.Toplevel(self.root)
        result_window.title("Encoded Data Output")
        result_window.attributes("-fullscreen", True)

        text_frame = tk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(text_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        result_text = tk.Text(text_frame, wrap="none", yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        result_text.pack(fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=result_text.yview)
        h_scrollbar.config(command=result_text.xview)

        result_text.insert(tk.END, result)

        tk.Button(result_window, text="Exit Fullscreen",
                  command=lambda: result_window.attributes("-fullscreen", False)).pack(pady=10)
