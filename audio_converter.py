import argparse
from pydub import AudioSegment
import os

# Set up argparse
parser = argparse.ArgumentParser(description="Convert an audio file to a specified format and extract a specific portion of the audio.")
parser.add_argument("input_file", help="Path to the input audio file (MP3 format).")
parser.add_argument("output_format", help="Desired output format (e.g., wav, mp3, flac).")
parser.add_argument("--start", type=int, default=0, help="Start time in milliseconds (default is 0).")
parser.add_argument("--end", type=int, default=None, help="End time in milliseconds (default is the duration of the audio).")

# Parse the arguments
args = parser.parse_args()

# Extract the base name from the input file (without extension)
base_name = os.path.splitext(os.path.basename(args.input_file))[0]

# Load the audio file
sound = AudioSegment.from_mp3(args.input_file)

# If end time is not specified, set it to the length of the audio
if args.end is None:
    args.end = len(sound)

# Slice the audio from start to end time
sound = sound[args.start:args.end]

# Construct the output file name with the same base name and new format
output_filename = f"{base_name}.{args.output_format}"

# Export the audio in the specified format
sound.export(output_filename, format=args.output_format)

print(f"Exported audio from {args.start}ms to {args.end}ms of {args.input_file} as {output_filename}.")
