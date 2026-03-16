import subprocess
import time
import sys
from pathlib import Path
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter


def run_spleeter(audio_file, output_dir):
    print("\nRunning Spleeter...")

    start = time.time()

    separator = Separator("spleeter:4stems")
    audio_loader = AudioAdapter.default()

    waveform, sr = audio_loader.load(audio_file)
    prediction = separator.separate(waveform)

    separator.save_to_file(prediction, audio_file, output_dir)

    end = time.time()
    print(f"Spleeter finished in {end-start:.2f} seconds")


def run_demucs(audio_file, output_dir):
    print("\nRunning Demucs...")

    start = time.time()

    subprocess.run(
        ["demucs", "-n", "htdemucs", "-o", output_dir, audio_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    end = time.time()
    print(f"Demucs finished in {end-start:.2f} seconds")


def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_spleeter_vs_demucs.py <audiofile>")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print("File not found.")
        return

    spleeter_output = "output_spleeter"
    demucs_output = "output_demucs"

    run_spleeter(audio_file, spleeter_output)
    run_demucs(audio_file, demucs_output)

if __name__ == "__main__":
    main()