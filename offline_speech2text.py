# How to install Whisper => https://github.com/openai/whisper

import whisper
import time
import argparse

# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description='Transcribe speech from an MP3 file using Whisper.')
parser.add_argument('--mp3_path', type=str, required=True, help='Path to the MP3 file')
parser.add_argument('--model_type', type=str, default='base', choices=['tiny', 'base', 'small', 'medium', 'large'], help='Type of the Whisper model')
parser.add_argument('--output_name', type=str, required=True, help='Path to save the output text file')
args = parser.parse_args()

model = whisper.load_model(args.model_type)
t0 = time.time()
result = model.transcribe(args.mp3_path)
t1 = time.time()
print(f'Completed in {(t1-t0):.1f} s')

with open(f'{args.output_name}.txt', 'w') as f:
    f.write(result['text'])
