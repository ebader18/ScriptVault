import argparse
from pydub import AudioSegment
import os

# Supported audio formats by pydub
supported_formats = ['mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a']

# Set up argparse
parser = argparse.ArgumentParser(description="Convert all audio files in a folder to a specified format.")
parser.add_argument("input_folder", help="Path to the folder containing audio files.")
parser.add_argument("output_format", help="Desired output format (e.g., wav, mp3, flac).")
parser.add_argument("--start", type=int, default=0, help="Start time in milliseconds (default is 0).")
parser.add_argument("--end", type=int, default=None, help="End time in milliseconds (default is the duration of the audio).")

# Parse the arguments
args = parser.parse_args()

# Validate the output format
if args.output_format not in supported_formats:
    print(f"Error: Unsupported output format '{args.output_format}'. Supported formats are: {', '.join(supported_formats)}")
    exit(1)

# Loop through all files in the input folder
for file_name in os.listdir(args.input_folder):
    input_file = os.path.join(args.input_folder, file_name)

    # Get the file extension and base name
    base_name, file_ext = os.path.splitext(file_name)
    file_ext = file_ext[1:].lower()  # Remove dot and convert to lowercase

    # Check if the file is an audio file and not already in the desired output format
    if file_ext in supported_formats and file_ext != args.output_format:
        # Load the audio file using pydub's appropriate method based on input format
        sound = AudioSegment.from_file(input_file, format=file_ext)

        # If end time is not specified, set it to the length of the audio
        if args.end is None:
            end_time = len(sound)
        else:
            end_time = args.end

        # Slice the audio from start to end time
        sound = sound[args.start:end_time]

        # Construct the output file path with the same base name and new format
        output_file = os.path.join(args.input_folder, f"{base_name}.{args.output_format}")

        # Check if the output file already exists
        if not os.path.exists(output_file):
            # Export the audio in the specified format
            sound.export(output_file, format=args.output_format)
            print(f"Converted {input_file} to {output_file}")
        else:
            print(f"Skipped {output_file}, already exists.")
    else:
        print(f"Skipped {input_file}, either not an audio file or already in the desired format.")
