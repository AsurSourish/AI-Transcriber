
from faster_whisper import WhisperModel
from tkinter import Tk, filedialog
from pathlib import Path
from datetime import datetime
import json
import time
import os


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02}:{minutes:02}:{secs:02}"


# -----------------------------
# File Picker
# -----------------------------

root = Tk()
root.withdraw()
root.attributes("-topmost", True)

print("Select an audio file...")

audio_path = filedialog.askopenfilename(
    title="Select Audio File",
    filetypes=[
        ("Audio Files", "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.mp4 *.mkv"),
        ("All Files", "*.*")
    ]
)

if not audio_path:
    print("No file selected.")
    raise SystemExit

audio_file = Path(audio_path)

# -----------------------------
# Folders
# -----------------------------

output_dir = Path("output")
logs_dir = Path("logs")

output_dir.mkdir(exist_ok=True)
logs_dir.mkdir(exist_ok=True)

base_name = audio_file.stem

transcript_file = output_dir / f"{base_name}_transcript.txt"
metadata_file = output_dir / f"{base_name}_metadata.json"

# -----------------------------
# Load Model
# -----------------------------

print("\nLoading Whisper model...")

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

print("Model loaded successfully")
print("GPU: CUDA")
print("Model: large-v3")
print("\nStarting transcription...\n")

# -----------------------------
# Transcription
# -----------------------------

start_time = time.time()

segments, info = model.transcribe(
    str(audio_file),
    beam_size=5,
    vad_filter=True
)

segment_count = 0

with open(transcript_file, "w", encoding="utf-8") as f:

    for segment in segments:
        segment_count += 1

        print(
            f"[{segment_count}] "
            f"{format_timestamp(segment.start)} "
            f"-> "
            f"{format_timestamp(segment.end)}"
        )

        f.write(
            f"[{format_timestamp(segment.start)}]\n"
            f"{segment.text.strip()}\n\n"
        )

elapsed = round(time.time() - start_time, 2)

# -----------------------------
# Metadata
# -----------------------------

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

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )

# -----------------------------
# Completion
# -----------------------------

print("\n========================")
print("TRANSCRIPTION COMPLETE")
print("========================")

print(f"\nLanguage Detected : {info.language}")
print(
    f"Confidence        : "
    f"{info.language_probability:.2%}"
)

print(f"\nSegments          : {segment_count}")
print(f"Processing Time   : {elapsed:.2f} sec")

print(f"\nTranscript File:")
print(transcript_file)

print(f"\nMetadata File:")
print(metadata_file)

print("\nOpening output folder...")

os.startfile(output_dir.resolve())
