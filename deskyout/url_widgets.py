import tkinter as tk
import pyperclip

class URLWidgets:
    def __init__(self, window):
        self.window = window

    def create_url_widgets(self):
        url_label = tk.Label(self.window, text="Enter YouTube URL:")
        url_label.pack()
        self.url_entry = tk.Entry(self.window)
        self.url_entry.pack()

        copy_button = tk.Button(self.window, text="Copy URL", command=self.copy_url)
        copy_button.pack()
        paste_button = tk.Button(self.window, text="Paste URL", command=self.paste_url)
        paste_button.pack()

    def copy_url(self):
        url = self.url_entry.get()
        if url:
            pyperclip.copy(url)

    def paste_url(self):
        url = pyperclip.paste()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
