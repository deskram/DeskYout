import tkinter as tk
from deskyout.url_widgets import URLWidgets
from deskyout.directory_widgets import DirectoryWidgets
from deskyout.action_buttons import ActionButtons


class DeskYout:
    def __init__(self, window):
        self.window = window
        self.window.title("DeskYout Downloader")
        self.window.geometry("400x440")
        self.url_widgets = URLWidgets(self.window)
        self.directory_widgets = DirectoryWidgets(self.window)
        self.action_buttons = ActionButtons(self.window, self.url_widgets, self.directory_widgets)

        self.create_widgets()

    def create_widgets(self):
        self.url_widgets.create_url_widgets()
        self.directory_widgets.create_directory_widgets()
        self.action_buttons.create_action_buttons()

