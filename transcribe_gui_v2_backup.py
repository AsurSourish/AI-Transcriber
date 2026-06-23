print("GUI FILE STARTED")


import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog
import os
from faster_whisper import WhisperModel
from datetime import datetime
import json
import time
import threading

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class AITranscriberGUI:

    def __init__(self):

        self.audio_path = None

        self.app = ctk.CTk()
        self.app.title("AI Transcriber")
        self.app.geometry("900x650")

        self.title = ctk.CTkLabel(
            self.app,
            text="AI Transcriber",
            font=("Segoe UI", 30, "bold")
        )
        self.title.pack(pady=25)

        self.file_label = ctk.CTkLabel(
            self.app,
            text="No file selected",
            font=("Segoe UI", 14)
        )
        self.file_label.pack(pady=10)

        self.select_btn = ctk.CTkButton(
            self.app,
            text="Select Audio",
            command=self.select_file,
            width=220,
            height=40
        )
        self.select_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.app,
            text="Start Transcription",
            state="disabled",
            command=self.start_transcription,
            width=220,
            height=40
        )
        self.start_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self.app,
            width=700
        )
        self.progress.pack(pady=25)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self.app,
            text="Status: Ready",
            font=("Segoe UI", 15)
        )
        self.status_label.pack(pady=10)

        self.gpu_label = ctk.CTkLabel(
            self.app,
            text="GPU: RTX 4060 (CUDA)",
            font=("Segoe UI", 14)
        )
        self.gpu_label.pack(pady=5)

        self.language_label = ctk.CTkLabel(
            self.app,
            text="Detected Language: Waiting...",
            font=("Segoe UI", 14)
        )
        self.language_label.pack(pady=5)

        self.time_label = ctk.CTkLabel(
            self.app,
            text="Elapsed Time: --",
            font=("Segoe UI", 14)
        )
        self.time_label.pack(pady=5)

        self.output_btn = ctk.CTkButton(
            self.app,
            text="Open Output Folder",
            command=self.open_output,
            width=220,
            height=40
        )
        self.output_btn.pack(pady=25)

        self.app.mainloop()

    def select_file(self):

        path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                (
                    "Audio Files",
                    "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.mp4 *.mkv"
                )
            ]
        )

        if path:
            self.audio_path = path

            filename = Path(path).name

            if len(filename) > 60:
                filename = filename[:57] + "..."

            self.file_label.configure(
                text=f"Selected: {filename}"
            )

            self.start_btn.configure(
                state="normal"
            )

    def start_transcription(self):

        print("BUTTON CLICKED")
        self.status_label.configure(
            text="Status: Button Working"
        )

        self.progress.set(0.25)

    def open_output(self):

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        os.startfile(output_dir.resolve())


AITranscriberGUI()

