# Interesting link: https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
#                   https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f

import cv2
import numpy as np
import argparse
import json
import os


def compute_intrinsic_distortion(images_path, pattern_size):
    # Parameters for the fisheye calibration
    termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points based on the chessboard size
    objp = np.zeros((np.prod(pattern_size), 1, 3), np.float32)
    objp[:, 0, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    for fname in images_path:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            objpoints.append(objp.astype(np.float32))  # Ensure it's in CV_32FC3 format

            # Refine the corners
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination_criteria)
            imgpoints.append(corners2)

    print(f'Found {len(objpoints)} good images out of {len(images_path)} total for calibration.')

    # Fisheye camera calibration
    K = np.zeros((3, 3), dtype=np.float64)
    D = np.zeros((4, 1), dtype=np.float64)
    rvecs = []
    tvecs = []

    img_shape = gray.shape[::-1]

    # Perform calibration using the fisheye module
    ret, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
        objpoints, imgpoints, img_shape, K, D, rvecs, tvecs,
        cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC | cv2.fisheye.CALIB_CHECK_COND | cv2.fisheye.CALIB_FIX_SKEW,
        termination_criteria
    )

    return K, D


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fisheye camera calibration using chessboard images.')
    parser.add_argument('--image_folder', type=str, required=True, help='Path to the folder containing calibration images.')
    parser.add_argument('--output_file', type=str, required=True, help='Name of the output JSON file to store calibration parameters.')
    parser.add_argument('--inner_corners_size', type=str, required=True, help='Number of inner corners in the format width,height (e.g., 9,6).')
    args = parser.parse_args()

    # Get list of image files in the specified folder
    images_path = [os.path.join(args.image_folder, f) for f in os.listdir(args.image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Parse pattern size
    pattern_size = tuple(map(int, args.inner_corners_size.split(',')))

    K, D = compute_intrinsic_distortion(images_path, pattern_size)

    # Save calibration parameters to JSON file
    calibration_data = {
        'K': K.tolist(),  # Intrinsic matrix
        'D': D.tolist()   # Distortion coefficients
    }
    with open(f'{args.output_file}.json', 'w') as json_file:
        json.dump(calibration_data, json_file, indent=4)

    print(f'Fisheye calibration parameters saved to {args.output_file}.json')


if __name__ == '__main__':
    main()
