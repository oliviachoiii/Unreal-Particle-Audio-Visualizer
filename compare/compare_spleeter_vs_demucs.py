import subprocess
import time
import sys
import librosa
import numpy as np
from pathlib import Path
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

def load_audio(path, sr=None, mono=False):
    y, actual_sr = librosa.load(path, sr=sr, mono=mono)
    if y.ndim == 1:
        y = y[np.newaxis, :]
    return y, actual_sr

def align_length(arrays):
    min_len = min(arr.shape[-1] for arr in arrays)
    return [arr[..., :min_len] for arr in arrays]


def reconstruction_mse(mixture_path, stems_dir, stem_names):
    mix, sr = load_audio(mixture_path, sr=None, mono=False)

    stem_arrays = []
    for stem in stem_names:
        stem_path = Path(stems_dir) / f"{stem}.wav"
        if not stem_path.exists():
            print(f"Warning: missing stem {stem_path}")
            continue

        y, _ = load_audio(str(stem_path), sr=sr, mono=False)
        stem_arrays.append(y)

    if not stem_arrays:
        return float("nan")

    aligned = align_length([mix] + stem_arrays)
    mix = aligned[0]
    stems = aligned[1:]

    summed = np.sum(np.stack(stems, axis=0), axis=0)
    err = mix - summed
    return float(np.mean(err ** 2))

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
    
    audio_stem_name = Path(audio_file).stem

    stem_names = ["vocals", "drums", "bass", "other"]

    spleeter_stems_dir = Path(spleeter_output) / audio_stem_name
    spleeter_mse = reconstruction_mse(audio_file, spleeter_stems_dir, stem_names)

    demucs_stems_dir = Path(demucs_output) / "htdemucs" / audio_stem_name
    demucs_mse = reconstruction_mse(audio_file, demucs_stems_dir, stem_names)

    print("\nReconstruction MSE Comparison:")
    print(f"Spleeter reconstruction MSE: {spleeter_mse:.8f}")
    print(f"Demucs reconstruction MSE:   {demucs_mse:.8f}")

    if spleeter_mse < demucs_mse:
        print("Spleeter has lower reconstruction MSE.")
    elif demucs_mse < spleeter_mse:
        print("Demucs has lower reconstruction MSE.")
    else:
        print("Both have the same reconstruction MSE.")

if __name__ == "__main__":
    main()