import cv2
import numpy as np
import argparse
import json
import os

# Set up argument parser
parser = argparse.ArgumentParser(description='Camera calibration using chessboard images.')
parser.add_argument('--image_folder', type=str, required=True, help='Path to the folder containing calibration images.')
parser.add_argument('--output_file', type=str, required=True, help='Name of the output JSON file to store calibration parameters.')
parser.add_argument('--pattern_size', type=str, required=True, help='Pattern size in the format width,height (e.g., 9,6).')
args = parser.parse_args()

# Parse pattern size
pattern_size = tuple(map(int, args.pattern_size.split(',')))

# Parameters
termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Get list of image files in the specified folder
images = [os.path.join(args.image_folder, f) for f in os.listdir(args.image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Prepare object points
objp = np.zeros((np.prod(pattern_size), 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Loop over images
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    # If found, add object points, image points
    if ret:
        objpoints.append(objp)

        # Refine the corners
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination_criteria)
        imgpoints.append(corners2)

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Extract parameters
fx = mtx[0, 0]
fy = mtx[1, 1]
cx = mtx[0, 2]
cy = mtx[1, 2]

# Prepare data for JSON output
calibration_data = {
    'fx': fx,
    'fy': fy,
    'cx': cx,
    'cy': cy
}

# Save parameters to JSON file
with open(f'{args.output_file}.json', 'w') as json_file:
    json.dump(calibration_data, json_file, indent=4)

print(f'Calibration parameters saved to {args.output_file}.')
