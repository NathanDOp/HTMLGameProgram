import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# Fixed folder path to scan
FOLDER_PATH = r"C:\Users\natha\PycharmProjects\HTMLOrganizer\HTMLs"  # Adjust this filepath to fit your device.

def list_html_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.html')]
        return sorted(files, key=lambda x: x.lower())
    except Exception as e:
        return []

def open_html_file(folder_path, filename):
    full_path = os.path.abspath(os.path.join(folder_path, filename))
    try:
        if sys.platform.startswith('darwin'):
            subprocess.run(['open', full_path])
        elif sys.platform.startswith('win'):
            os.startfile(full_path)
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', full_path])
        else:
            messagebox.showerror("Error", f"Unsupported OS: {sys.platform}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")

class HtmlFileSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HTML File Selector")
        self.geometry("480x320")
        self.resizable(False, False)

        # Label showing folder path
        self.folder_label = ttk.Label(self, text=f"Folder: {FOLDER_PATH}", wraplength=460)
        self.folder_label.pack(padx=10, pady=(10,5))

        # Listbox with vertical scrollbar
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=5, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(frame, orient="vertical")
        self.listbox = tk.Listbox(frame, height=12, yscrollcommand=self.scrollbar.set, activestyle='dotbox',
                                  font=('Segoe UI', 11))
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Buttons frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.open_btn = ttk.Button(btn_frame, text="Open Selected", command=self.open_selected)
        self.open_btn.grid(row=0, column=0, padx=5)

        self.refresh_btn = ttk.Button(btn_frame, text="Refresh List", command=self.refresh_list)
        self.refresh_btn.grid(row=0, column=1, padx=5)

        # Populate listbox on startup
        self.refresh_list()

        # Bind double-click event on listbox items
        self.listbox.bind('<Double-1>', self.on_double_click)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        files = list_html_files(FOLDER_PATH)
        if not files:
            messagebox.showinfo("No HTML Files", "No HTML files found in the folder.")
        else:
            for f in files:
                self.listbox.insert(tk.END, f)

    def open_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file from the list.")
            return
        filename = self.listbox.get(selection[0])
        open_html_file(FOLDER_PATH, filename)

    def on_double_click(self, event):
        self.open_selected()

if __name__ == "__main__":
    if not os.path.isdir(FOLDER_PATH):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Invalid Folder", f"The folder path does not exist:\n{FOLDER_PATH}")
        sys.exit(1)

    app = HtmlFileSelectorApp()
    app.mainloop()
