import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog
from faster_whisper import WhisperModel
from datetime import datetime
import threading
import json
import time
import os

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02}:{minutes:02}:{secs:02}"

class AITranscriberGUI:

    def __init__(self):

        self.audio_path = None
        self.start_time = None

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("AI Transcriber V3")
        self.app.geometry("900x650")

        self.title = ctk.CTkLabel(
            self.app,
            text="AI Transcriber",
            font=("Segoe UI", 30, "bold")
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
            command=self.select_file,
            width=220
        )
        self.select_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.app,
            text="Start Transcription",
            state="disabled",
            command=self.start_transcription,
            width=220
        )
        self.start_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self.app,
            width=700
        )
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self.app,
            text="Status: Ready"
        )
        self.status_label.pack(pady=5)

        self.gpu_label = ctk.CTkLabel(
            self.app,
            text="GPU: RTX 4060 (CUDA)"
        )
        self.gpu_label.pack(pady=5)

        self.language_label = ctk.CTkLabel(
            self.app,
            text="Language: Waiting..."
        )
        self.language_label.pack(pady=5)

        self.time_label = ctk.CTkLabel(
            self.app,
            text="Elapsed Time: --"
        )
        self.time_label.pack(pady=5)

        self.output_btn = ctk.CTkButton(
            self.app,
            text="Open Output Folder",
            command=self.open_output
        )
        self.output_btn.pack(pady=20)

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

            if len(filename) > 70:
                filename = filename[:67] + "..."

            self.file_label.configure(
                text=f"Selected: {filename}"
            )

            self.start_btn.configure(
                state="normal"
            )

    def start_transcription(self):

        if not self.audio_path:
            return

        self.start_btn.configure(
            state="disabled"
        )

        threading.Thread(
            target=self.run_transcription,
            daemon=True
        ).start()
        
        

    
        
    def run_transcription(self):

        try:

            self.status_label.configure(
                text="Status: Loading Whisper..."
            )

            self.progress.set(0.10)

            audio_file = Path(self.audio_path)

            output_dir = Path("output")
            logs_dir = Path("logs")

            output_dir.mkdir(exist_ok=True)
            logs_dir.mkdir(exist_ok=True)

            base_name = audio_file.stem

            transcript_file = (
                output_dir /
                f"{base_name}_transcript.txt"
            )

            metadata_file = (
                output_dir /
                f"{base_name}_metadata.json"
            )

            model = WhisperModel(
                "large-v3",
                device="cuda",
                compute_type="float16"
            )

            self.status_label.configure(
                text="Status: Transcribing..."
            )

            self.progress.set(0.25)

            start_time = time.time()

            segments, info = model.transcribe(
                str(audio_file),
                beam_size=5,
                vad_filter=True
            )

            segment_count = 0

            with open(
                transcript_file,
                "w",
                encoding="utf-8"
            ) as f:

                for segment in segments:

                    segment_count += 1

                    f.write(
                        f"[{format_timestamp(segment.start)}]\n"
                        f"{segment.text.strip()}\n\n"
                    )

            elapsed = round(
                time.time() - start_time,
                2
            )

            self.progress.set(0.80)

            metadata = {
                "file": audio_file.name,
                "model": "large-v3",
                "device": "cuda",
                "compute_type": "float16",
                "language": info.language,
                "language_probability": round(
                    info.language_probability,
                    4
                ),
                "segments": segment_count,
                "processing_time_seconds": elapsed,
                "processing_time_minutes": round(
                    elapsed / 60,
                    2
                ),
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            with open(
                metadata_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    metadata,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            self.progress.set(1.0)

            self.language_label.configure(
                text=(
                    f"Language: "
                    f"{info.language} "
                    f"({info.language_probability:.1%})"
                )
            )

            self.time_label.configure(
                text=f"Elapsed Time: {elapsed:.2f}s"
            )

            self.status_label.configure(
                text="Status: Complete"
            )

            os.startfile(output_dir.resolve())

        except Exception as e:

            self.status_label.configure(
                text=f"Error: {str(e)}"
            )

        finally:

            self.start_btn.configure(
                state="normal"
            )

    def open_output(self):

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        os.startfile(output_dir.resolve())

    def run(self):

        self.app.mainloop()

if __name__ == "__main__":

    app = AITranscriberGUI()
    app.run()