# Interesting link: https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
#                   https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f


import cv2
import json
import argparse
import numpy as np


def undistort(img, K, D, balance=0.0, dim2=None, dim3=None):
    dim1 = img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim2, np.eye(3), balance=balance)
    mapx, mapy = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    # Display both the original and corrected images side by side
    concatenated = np.hstack((img, undistorted_img))

    return concatenated

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Show non-corrected and fisheye-corrected images using calibration parameters.')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the input image.')
    parser.add_argument('--calibration_path', type=str, required=True, help='Path to the JSON file containing fisheye calibration parameters.')
    args = parser.parse_args()

    # Load image
    img = cv2.imread(args.image_path)
    if img is None:
        print(f"Error: Could not read image from {args.image_path}")
        exit()

    # Load calibration parameters from JSON file
    with open(args.calibration_path, 'r') as f:
        calib = json.load(f)

    K = np.array(calib['K'])
    D = np.array(calib['D'])
    concatenated = undistort(img, K, D, balance=1.0)

    cv2.imshow('Original (Left) vs Fisheye Corrected (Right)', concatenated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
