import tkinter as tk
from tkinter import ttk, scrolledtext
from pytube import YouTube, Playlist
import os
import threading
import time

class ActionButtons:
    def __init__(self, window, url_widgets, directory_widgets):
        self.window = window
        self.url_widgets = url_widgets
        self.directory_widgets = directory_widgets
        self.progress_bar = None
        self.format_choice = tk.IntVar()
        self.quality_choice = tk.IntVar()

    def create_action_buttons(self):
        download_button = tk.Button(self.window, text="Download", command=self.download)
        download_button.pack()
        status_text = scrolledtext.ScrolledText(self.window, height=8, width=50)
        status_text.pack()
        self.status_text = status_text
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        format_frame = ttk.Frame(self.window)
        format_frame.pack(pady=10)
        format_label = ttk.Label(format_frame, text="Format:")
        format_label.pack(side="left")
        video_format = ttk.Radiobutton(format_frame, text="Video", variable=self.format_choice, value=1)
        video_format.pack(side="left")
        audio_format = ttk.Radiobutton(format_frame, text="Audio", variable=self.format_choice, value=2)
        audio_format.pack(side="left")

        quality_frame = ttk.Frame(self.window)
        quality_frame.pack(pady=10)
        quality_label = ttk.Label(quality_frame, text="Quality:")
        quality_label.pack(side="left")
        highest_quality = ttk.Radiobutton(quality_frame, text="Highest", variable=self.quality_choice, value=1)
        highest_quality.pack(side="left")
        lowest_quality = ttk.Radiobutton(quality_frame, text="Lowest", variable=self.quality_choice, value=2)
        lowest_quality.pack(side="left")

        self.status_text.tag_config("blue", foreground="blue")
        self.status_text.tag_config("red", foreground="red")
        self.status_text.tag_config("green", foreground="green")
        self.status_text.tag_config("orange", foreground="orange")

    def display_status(self, text, color):
        self.status_text.configure(state='normal')
        self.status_text.insert(tk.END, text + '\n', color)
        self.status_text.configure(state='disabled')
        self.status_text.see(tk.END)

    def download(self):
        url = self.url_widgets.url_entry.get()
        if not url:
            self.display_status("Please enter a YouTube URL.", "red")
            return
        save_directory = self.directory_widgets.directory_entry.get()
        if not save_directory:
            self.display_status("Please select a download directory.", "red")
            return
        threading.Thread(target=self.process_download, args=(url, save_directory)).start()

    def process_download(self, url, save_directory):
        if 'playlist?list=' in url:
            self.download_playlist(url, save_directory)
        elif 'watch?v=' in url or 'youtu.be/' in url or 'live/' in url:
            self.download_video(url, save_directory)
        else:
            self.display_status("Invalid YouTube URL.", "red")

    def download_playlist(self, url, save_directory):
        try:
            playlist = Playlist(url)
            playlist_title = playlist.title
            playlist_directory = os.path.join(save_directory, playlist_title)
            os.makedirs(playlist_directory, exist_ok=True)
            self.display_status(f"Downloading playlist '{playlist_title}'...", "blue")
            videos = playlist.video_urls
            total_videos = len(videos)
            self.display_status(f"Total videos in playlist: {total_videos}", "blue")
            for index, video_url in enumerate(videos):
                self.update_progress(index, total_videos)
                while True:
                    try:
                        self.download_video(video_url, playlist_directory, index + 1, True)
                        break
                    except Exception as e:
                        self.display_status(f"Error downloading video {index + 1}. Retrying...", "red")
                        print(str(e))
            self.display_status("Download completed.", "green")
            self.progress_bar["value"] = 0
        except Exception as e:
            self.display_status("Error occurred during playlist download.", "red")
            print(str(e))

    def download_video(self, url, save_directory, index=None, is_playlist=False):
        try:
            video = YouTube(url)
            video_title = video.title
            file_name = f"{index} - {video_title}.mp4" if is_playlist else f"{video_title}.mp4"
            if os.path.exists(os.path.join(save_directory, file_name)):
                self.display_status(f"Skipping video {index} - {video_title}, already exists.", "orange" if is_playlist else "blue")
                return
            start_time = time.time()
            self.display_status(f"Downloading video {index} - {video_title}..." if is_playlist else f"Downloading video {video_title}...", "blue")
            format_choice = self.format_choice.get()
            quality_choice = self.quality_choice.get()
            if format_choice == 1:
                stream = self.get_video_stream(video, quality_choice)
            elif format_choice == 2:
                stream = self.get_audio_stream(video)
            else:
                self.display_status("Invalid format choice.", "red")
                return
            stream.download(output_path=save_directory, filename_prefix=f"{index} - " if is_playlist else "")
            elapsed_time = time.time() - start_time
            self.display_status(f"Download of video {index} - {video_title} completed in {elapsed_time:.2f} seconds." if is_playlist else f"Download of video {video_title} completed in {elapsed_time:.2f} seconds.", "green")
        except Exception as e:
            self.display_status(f"Error occurred during download of video {index if is_playlist else ''}.", "red")
            print(str(e))

    def get_video_stream(self, video, quality_choice):
        if quality_choice == 1:
            return video.streams.get_highest_resolution()
        elif quality_choice == 2:
            return video.streams.get_lowest_resolution()
        else:
            raise ValueError("Invalid quality choice.")

    def get_audio_stream(self, video):
        return video.streams.filter(only_audio=True).first()

    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress_bar["value"] = percentage
        self.window.update()
