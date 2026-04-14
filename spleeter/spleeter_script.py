import sys
import numpy as np
import soundfile as sf
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from pathlib import Path

# To run this script, ensure you have Spleeter installed: # https://github.com/deezer/spleeter/wiki/1.-Installation # This script takes an input audio file and separates it into 5 stems: vocals, drums, bass, piano, and other. # Usage: # python separate.py <audiofile> [output_dir] # Note: when ran, will download the 5-stem model if not already present in /pretrained_models/... # Do not push the downloaded model to GitHub, as it is large.

# This script separates an input song into 5 stems using Spleeter:
# vocals, drums, bass, piano, other
#
# It saves:
# 1. normal aligned stems
# 2. trimmed stems with leading silence removed
#
# Usage:
# python separate.py <audiofile> [output_dir]

def trim_leading_silence(audio, threshold=0.01):
    if audio.ndim == 1:
        envelope = np.abs(audio)
    else:
        envelope = np.max(np.abs(audio), axis=1)

    non_silent_indices = np.where(envelope > threshold)[0]

    if len(non_silent_indices) == 0:
        return audio 

    start_idx = non_silent_indices[0]
    return audio[start_idx:]


def save_stem(audio_loader, path, audio_data, sample_rate):
    audio_loader.save(str(path), audio_data, sample_rate, codec="wav")


def save_trimmed_stem(path, audio_data, sample_rate):
    sf.write(str(path), audio_data, sample_rate)


def separate_audio(input_file, output_dir="output"):
    # Load the 5-stem model
    separator = Separator("spleeter:5stems")

    # Load audio
    audio_loader = AudioAdapter.default()
    waveform, sample_rate = audio_loader.load(input_file, sample_rate=44100)

    # Run separation
    prediction = separator.separate(waveform)

    # Output folders
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    base_name = Path(input_file).stem

    normal_folder = output_path / base_name / "normal"
    trimmed_folder = output_path / base_name / "trimmed"

    normal_folder.mkdir(parents=True, exist_ok=True)
    trimmed_folder.mkdir(parents=True, exist_ok=True)

    stem_names = ["vocals", "drums", "bass", "piano", "other"]

    # Save both normal and trimmed stems
    for stem in stem_names:
        stem_audio = prediction[stem]

        normal_path = normal_folder / f"{stem}.wav"
        trimmed_path = trimmed_folder / f"{stem}.wav"

        # Save original aligned stem
        save_stem(audio_loader, normal_path, stem_audio, sample_rate)

        # Trim leading silence and save
        trimmed_audio = trim_leading_silence(stem_audio, threshold=0.01)
        save_trimmed_stem(trimmed_path, trimmed_audio, sample_rate)

    print(f"Normal stems saved in:  {normal_folder}")
    print(f"Trimmed stems saved in: {trimmed_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python separate.py <audiofile> [output_dir]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    separate_audio(input_file, output_dir)