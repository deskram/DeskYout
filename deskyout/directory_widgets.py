import tkinter as tk
from tkinter import filedialog

class DirectoryWidgets:
    def __init__(self, window):
        self.window = window

    def create_directory_widgets(self):
        directory_label = tk.Label(self.window, text="Save Directory:")
        directory_label.pack()
        self.directory_entry = tk.Entry(self.window)
        self.directory_entry.pack()

        browse_button = tk.Button(self.window, text="Browse", command=self.browse_directory)
        browse_button.pack()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
