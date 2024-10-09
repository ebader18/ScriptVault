import cv2
import argparse

def trim_video(input_path, start_time, end_time, output_path):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    
    # Get the video's frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the start and end frames based on the FPS
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Check if start and end frames are within the video length
    if start_frame >= total_frames or end_frame > total_frames:
        print("Start or end time exceeds the length of the video.")
        return

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, 
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                           int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # Read and write frames until the end frame
    current_frame = start_frame
    while cap.isOpened() and current_frame < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Release resources
    cap.release()
    out.release()
    print(f"Video trimmed successfully: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Trim a video using OpenCV.')
    parser.add_argument('input_path', type=str, help='Path to the input video file')
    parser.add_argument('start_time', type=float, help='Start time in seconds')
    parser.add_argument('end_time', type=float, help='End time in seconds')
    parser.add_argument('output_path', type=str, help='Path to save the trimmed video')

    args = parser.parse_args()

    trim_video(args.input_path, args.start_time, args.end_time, args.output_path)

if __name__ == '__main__':
    main()
