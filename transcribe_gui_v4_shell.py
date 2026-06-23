import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog
import os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class AITranscriberGUI:

    def __init__(self):

        self.audio_path = None

        self.app = ctk.CTk()
        self.app.title("AI Transcriber")
        self.app.geometry("700x500")

        self.title = ctk.CTkLabel(
            self.app,
            text="AI Transcriber",
            font=("Segoe UI", 28, "bold")
        )
        self.title.pack(pady=20)

        self.file_label = ctk.CTkLabel(
            self.app,
            text="No file selected"
        )
        self.file_label.pack(pady=10)

        self.select_btn = ctk.CTkButton(
            self.app,
            text="Select Audio",
            command=self.select_file
        )
        self.select_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.app,
            text="Start Transcription",
            state="disabled"
        )
        self.start_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.app)
        self.progress.pack(fill="x", padx=30, pady=20)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self.app,
            text="Status: Ready"
        )
        self.status_label.pack(pady=10)

        self.gpu_label = ctk.CTkLabel(
            self.app,
            text="GPU: RTX 4060 (CUDA)"
        )
        self.gpu_label.pack(pady=5)

        self.language_label = ctk.CTkLabel(
            self.app,
            text="Detected Language: Waiting..."
        )
        self.language_label.pack(pady=5)

        self.time_label = ctk.CTkLabel(
            self.app,
            text="Estimated Remaining: --"
        )
        self.time_label.pack(pady=5)

        self.output_btn = ctk.CTkButton(
            self.app,
            text="Open Output Folder",
            command=self.open_output
        )
        self.output_btn.pack(pady=20)

        self.app.mainloop()

    def select_file(self):

        path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files",
                 "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.mp4 *.mkv")
            ]
        )

        if path:
            self.audio_path = path
            self.file_label.configure(
                text=f"Selected: {Path(path).name}"
            )
            self.start_btn.configure(state="normal")

    def open_output(self):

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        os.startfile(output_dir.resolve())


AITranscriberGUI()