import os
import argparse
from PIL import Image

# Function to convert images
def convert_images(input_folder, output_folder, output_format):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".bmp"):
            # Construct the full input and output file paths
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + f".{output_format}"
            output_path = os.path.join(output_folder, output_filename)

            # Open and convert the BMP image to the specified output format
            with Image.open(input_path) as img:
                img.save(output_path, output_format.upper())

    print("Conversion complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert BMP images to the specified format.")
    parser.add_argument("input_folder", help="Path to the input folder containing BMP images")
    parser.add_argument("output_format", help="Desired output format (e.g., 'png', 'jpeg')")
    args = parser.parse_args()

    # Automatically create the 'output' folder
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Call the function to convert images
    convert_images(args.input_folder, output_folder, args.output_format)
