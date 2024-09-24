import cv2
import argparse
import os


def convert_video(input_path, output_extension, codec):
    # Capture the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {input_path}")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = os.path.splitext(input_path)[0] + '.' + output_extension
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Read until video is completed
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Write the frame into the file
            out.write(frame)
        else:
            break

    # Release everything when job is finished
    cap.release()
    out.release()
    print(f"Converted video saved as: {output_path}")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Convert video to a different format.")
    parser.add_argument("input_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_extension", type=str, help="Extension of the output video format (e.g., mp4, avi).")
    parser.add_argument("codec", type=str, help="Four character code for codec. Options include: 'XVID' (AVI), 'MP4V' (MP4), 'H264' (MP4/AVI), 'H265' (MP4), 'MJPG' (AVI), etc.")
    args = parser.parse_args()

    # Convert video
    convert_video(args.input_path, args.output_extension, args.codec)


if __name__ == '__main__':
    main()
