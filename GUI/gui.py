import tkinter as tk
from tkinter import messagebox
import os
import data_encoding


DATASET_PATH = "/home/aliksmn/PycharmProjects/machine_learning/datasets"


def load_datasets():
    try:
        files = [f for f in os.listdir(DATASET_PATH) if f.endswith('.txt')]
        return files
    except Exception as e:
        messagebox.showerror("Error", f"Error loading datasets: {str(e)}")
        return []


def on_dataset_select(event):
    selected_file = dataset_var.get()
    if selected_file:
        try:
            file_path = os.path.join(DATASET_PATH, selected_file)
            headers = data_encoding.get_headers(file_path)
            target_dropdown['menu'].delete(0, 'end')
            for header in headers:
                target_dropdown['menu'].add_command(
                    label=header, command=tk._setit(target_var, header)
                )
            target_var.set(headers[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")


def run_program():
    selected_file = dataset_var.get()
    target_variable = target_var.get()

    if not selected_file or not target_variable:
        messagebox.showerror("Error", "Please select a dataset and target variable.")
        return

    try:
        file_path = os.path.join(DATASET_PATH, selected_file)
        result = data_encoding.process_file(file_path, target_variable)

        result_window = tk.Toplevel(root)
        result_window.title("Encoded Data Output")
        result_window.attributes('-fullscreen', True)

        text_frame = tk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(text_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        result_text = tk.Text(
            text_frame, wrap="none", width=100, height=30,
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=result_text.yview)
        h_scrollbar.config(command=result_text.xview)

        result_text.insert(tk.END, result)

        close_button = tk.Button(
            result_window, text="Exit Fullscreen",
            command=lambda: result_window.attributes('-fullscreen', False)
        )
        close_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def on_escape(event):
    root.attributes('-fullscreen', False)


root = tk.Tk()
root.title("Dataset Processor")

root.geometry("600x400")

dataset_var = tk.StringVar()
dataset_var.set("Select a dataset")

target_var = tk.StringVar()
target_var.set("Select a target variable")

datasets = load_datasets()

dataset_label = tk.Label(root, text="Select Dataset:")
dataset_label.pack(pady=10)

dataset_dropdown = tk.OptionMenu(root, dataset_var, *datasets, command=on_dataset_select)
dataset_dropdown.pack(pady=5)

target_label = tk.Label(root, text="Select Target Variable:")
target_label.pack(pady=10)

target_dropdown = tk.OptionMenu(root, target_var, ())
target_dropdown.pack(pady=5)

run_button = tk.Button(root, text="Run Program", command=run_program)
run_button.pack(pady=20)

root.attributes('-fullscreen', True)

root.bind("<Escape>", on_escape)

root.mainloop()
