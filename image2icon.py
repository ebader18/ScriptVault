import argparse
from PIL import Image

def convert_png_to_ico(png_image_path, ico_image_path):
    # Open the PNG image using Pillow
    img = Image.open(png_image_path)

    # Convert the image to an ICO file with multiple sizes
    img.save(ico_image_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])
    
    print(f'Converted {png_image_path} to {ico_image_path}')

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert PNG image to ICO format.')
    
    # Add arguments for input PNG file and output ICO file
    parser.add_argument('png_image', help='Path to the input PNG image')
    parser.add_argument('ico_image', help='Path for the output ICO file')

    # Parse the arguments
    args = parser.parse_args()

    # Call the conversion function with the parsed arguments
    convert_png_to_ico(args.png_image, args.ico_image)

if __name__ == '__main__':
    main()
