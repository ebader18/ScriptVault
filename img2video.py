import cv2
import os
import argparse
from tqdm import tqdm

def images_to_video(folder_path, output_path):
    # Get sorted list of images
    images = sorted([img for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))])

    if not images:
        print("No images found in the specified folder.")
        return
    
    # Read the first image to get dimensions
    first_image_path = os.path.join(folder_path, images[0])
    first_image = cv2.imread(first_image_path)
    height, width, _ = first_image.shape

    # Extract file extension from output path
    output_format = os.path.splitext(output_path)[1].lower()

    # Define the codec based on the chosen format
    fourcc_dict = {
        '.mp4': 'mp4v',  # 'XVID' or 'avc1' may also work
        '.avi': 'XVID',
        '.mov': 'mp4v'
    }
    
    fourcc = fourcc_dict.get(output_format, 'mp4v')  # Default to mp4v if unknown format

    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*fourcc), 30, (width, height))

    print(f"Creating video '{output_path}' with {len(images)} frames...")

    # Use tqdm for progress bar
    for image_name in tqdm(images, desc="Processing Frames", unit="frame"):
        image_path = os.path.join(folder_path, image_name)
        frame = cv2.imread(image_path)
        
        if frame is None:
            print(f"Skipping invalid image: {image_name}")
            continue
        
        video_writer.write(frame)

    video_writer.release()
    print(f"✅ Video saved as {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images from a folder into a video with progress tracking.")
    parser.add_argument("folder", help="Path to the folder containing images")
    parser.add_argument("output", help="Full path of the output video file (including name and extension)")

    args = parser.parse_args()
    images_to_video(args.folder, args.output)
