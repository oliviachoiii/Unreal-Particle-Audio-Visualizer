import sys
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from pathlib import Path

# To run this script, ensure you have Spleeter installed:
# https://github.com/deezer/spleeter/wiki/1.-Installation

# This script takes an input audio file and separates it into 4 stems: vocals, drums, bass, and other.
# Usage:
# python separate.py <audiofile> [output_dir]

# Note: when ran, will download the 4-stem model if not already present in /pretrained_models/...
# Do not push the downloaded model to GitHub, as it is large.

def separate_audio(input_file, output_dir="output"):
    # Load the 4-stem model
    separator = Separator('spleeter:4stems')

    # Load audio
    audio_loader = AudioAdapter.default()
    waveform, sample_rate = audio_loader.load(input_file, sample_rate=44100)

    # Run separation
    prediction = separator.separate(waveform)

    # Save outputs
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    base_name = Path(input_file).stem
    track_folder = output_path / base_name
    track_folder.mkdir(exist_ok=True)

    audio_loader.save(str(track_folder / "vocals.wav"), prediction['vocals'], sample_rate, codec='wav')
    audio_loader.save(str(track_folder / "drums.wav"), prediction['drums'], sample_rate, codec='wav')
    audio_loader.save(str(track_folder / "bass.wav"), prediction['bass'], sample_rate, codec='wav')
    audio_loader.save(str(track_folder / "other.wav"), prediction['other'], sample_rate, codec='wav')

    print(f"Separated tracks saved in: {track_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python separate.py <audiofile> [output_dir]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    separate_audio(input_file, output_dir)