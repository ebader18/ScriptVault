import cv2
import json
import argparse
import numpy as np

# Set up argument parser
parser = argparse.ArgumentParser(description='Show non-corrected and fisheye-corrected images using calibration parameters.')
parser.add_argument('--image', type=str, required=True, help='Path to the input image.')
parser.add_argument('--calibration_file', type=str, required=True, help='Path to the JSON file containing fisheye calibration parameters.')
args = parser.parse_args()

# Load the image
img = cv2.imread(args.image)
if img is None:
    print(f"Error: Could not read image from {args.image}")
    exit()

# Load calibration parameters from JSON file
with open(args.calibration_file, 'r') as f:
    calib_data = json.load(f)

# Extract the intrinsic matrix and distortion coefficients
K = np.array(calib_data['K'])
D = np.array(calib_data['D'])

# Get the image size
h, w = img.shape[:2]

# Compute undistortion map using the fisheye module
mapx, mapy = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, (w, h), cv2.CV_32FC1)
undistorted_img = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR)

# Resize the undistorted image to match the original for display purposes
undistorted_img_resized = cv2.resize(undistorted_img, (img.shape[1], img.shape[0]))

# Display both the original and corrected images side by side
concatenated = np.hstack((img, undistorted_img_resized))

# Show the images
cv2.imshow('Original (Left) vs Fisheye Corrected (Right)', concatenated)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
