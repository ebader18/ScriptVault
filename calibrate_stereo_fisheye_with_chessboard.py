import cv2
import numpy as np
import argparse
import json
import os, glob


# Check for NaNs or infs in points
def check_points_validity(points):
    for i, p in enumerate(points):
        if np.isnan(p).any() or np.isinf(p).any():
            print(f"Invalid values found in points at index {i}")
            return False
    return True


def stereo_fisheye_calibrate(left_image_folder, right_image_folder, pattern_size, K_left, D_left, K_right, D_right):
    # Prepare object points (real-world coordinates for chessboard corners)
    objp = np.zeros((np.prod(pattern_size), 1, 3), np.float32)
    objp[:, 0, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points
    objpoints = []  # 3D points in real world space
    left_imgpoints = []  # 2D points for the left camera
    right_imgpoints = []  # 2D points for the right camera

    # Load left and right image paths
    # left_images = sorted(glob.glob(left_image_folder + '/*.png'))
    # right_images = sorted(glob.glob(right_image_folder + '/*.png'))

    # Make sure the number of images matches
    if len(left_image_folder) != len(right_image_folder):
        print("Error: The number of left and right images must be the same.")
        return None, None, None, None

    # Ensure the mask has the correct length
    # if len(mask) != len(left_image_folder):
    #    print(f"Error: Mask length {len(mask)} does not match the number of image pairs {len(left_image_folder)}.")
    #    return None, None, None, None

    mask = np.ones(33)
    # mask[0:15] = 0
    # Loop through each image pair, using the mask to decide whether to include the image or not
    for i, (left_img_path, right_img_path) in enumerate(zip(left_image_folder, right_image_folder)):
        if mask[i]:
            # Read the images
            img_left = cv2.imread(left_img_path)
            img_right = cv2.imread(right_img_path)

            # Convert to grayscale
            gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
            gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

            # Find chessboard corners in both images
            ret_left, corners_left = cv2.findChessboardCorners(gray_left, pattern_size, None)
            ret_right, corners_right = cv2.findChessboardCorners(gray_right, pattern_size, None)

            if ret_left and ret_right:
                '''if ret_left:
                    cv2.drawChessboardCorners(img_left, pattern_size, corners_left, ret_left)
                    cv2.putText(img_left, left_img_path, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 1)
                    cv2.imshow('Left Chessboard', img_left)
                if ret_right:
                    cv2.putText(img_right, right_img_path, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 1)
                    cv2.drawChessboardCorners(img_right, pattern_size, corners_right, ret_right)
                    cv2.imshow('Right Chessboard', img_right)
                cv2.waitKey(0)  # Wait for a key press to proceed to the next image pair'''

                # Refine corner detection
                corners_left = cv2.cornerSubPix(gray_left, corners_left, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
                corners_right = cv2.cornerSubPix(gray_right, corners_right, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

                # Append object points and image points
                objpoints.append(objp)
                left_imgpoints.append(corners_left)
                right_imgpoints.append(corners_right)

                '''# print("Checking object points for validity...")
                if not check_points_validity(objpoints):
                    print("Error: Invalid object points detected.")
                    return None, None, None, None

                # print("Checking left image points for validity...")
                if not check_points_validity(left_imgpoints):
                    print("Error: Invalid left image points detected.")
                    return None, None, None, None

                # print("Checking right image points for validity...")
                if not check_points_validity(right_imgpoints):
                    print("Error: Invalid right image points detected.")
                    return None, None, None, None'''

                '''if len(objpoints) == len(left_imgpoints) == len(right_imgpoints):
                    print("Points arrays are of equal length.")
                else:
                    print("Error: Points arrays have mismatched lengths.")'''
            else:
                print(f"Chessboard not found in pair: {left_img_path} and {right_img_path}")

    # Check if any valid pairs are left after applying the mask
    if len(objpoints) == 0:
        print("No valid image pairs to process after applying the mask.")
        return None, None, None, None

    # Stereo calibration
    R = np.zeros((3, 3))  # Rotation matrix between the two cameras
    T = np.zeros((3, 1))  # Translation vector between the two cameras
    E = np.zeros((3, 3))  # Essential matrix
    F = np.zeros((3, 3))  # Fundamental matrix

    # Perform stereo calibration using the fisheye model
    # D_left = np.zeros((4, 1))  # Disable distortion for testing
    # D_right = np.zeros((4, 1))  # Disable distortion for testing
    # flags = cv2.fisheye.CALIB_FIX_INTRINSIC
    flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND
    ret, R, T, E, F = cv2.fisheye.stereoCalibrate(
        objpoints, left_imgpoints, right_imgpoints,
        K_left, D_left, K_right, D_right,
        gray_left.shape[::-1],  # Numpy wants [h, w] whereas OpenCV wants [w, h]
        R, T, E, F,
        flags=flags
    )
    if not ret:
        print("Stereo calibration failed with status:", ret)
    else:
        print("Stereo calibration succeeded.")

    return R, T, E, F


def main():
    # Argument parsing
    '''parser = argparse.ArgumentParser(description='Stereo camera calibration to compute extrinsic parameters.')
    parser.add_argument('--left_image_folder', type=str, required=True, help='Path to the folder containing left camera images.')
    parser.add_argument('--right_image_folder', type=str, required=True, help='Path to the folder containing right camera images.')
    parser.add_argument('--inner_corners_size', type=str, required=True, help='Number of inner corners in the format width,height (e.g., 9,6).')
    parser.add_argument('--output_file', type=str, required=True, help='Name of the output JSON file to store stereo calibration parameters.')
    args = parser.parse_args()'''

    left_image_folder = 'C:/_sw/ScriptVault/left'
    right_image_folder = 'C:/_sw/ScriptVault/right'
    inner_corners_size = '8,5'
    output_file = 'stereo_1280_960'

    # Parse chessboard pattern size
    # pattern_size = tuple(map(int, args.inner_corners_size.split(',')))
    pattern_size = tuple(map(int, inner_corners_size.split(',')))

    # Get list of left and right image files
    # left_images = sorted([os.path.join(args.left_image_folder, f) for f in os.listdir(args.left_image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    left_images = sorted([os.path.join(left_image_folder, f) for f in os.listdir(left_image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    # right_images = sorted([os.path.join(args.right_image_folder, f) for f in os.listdir(args.right_image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    right_images = sorted([os.path.join(right_image_folder, f) for f in os.listdir(right_image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    if len(left_images) != len(right_images):
        print("Error: The number of left and right images must be the same.")
        exit()

    # Example intrinsic parameters (K and D) for left and right cameras
    # Replace these with the actual intrinsic parameters
    K_left = np.array([[843.3145130977939, 0.0, 691.6739762797115], [0.0, 845.010519490556, 534.8871258189922], [0.0, 0.0, 1.0]])
    D_left = np.array([[-0.09389334257474875], [-0.012962011659942653], [0.0010999745465497517], [-0.0007379412335717166]])
    K_right = np.array([[850.7284870345256, 0.0, 682.6994840323507], [0.0, 852.5755999114342, 500.5756930163937], [0.0, 0.0, 1.0]])
    D_right = np.array([[-0.08555033917013267], [-0.04322699046179681], [0.05994203739853651], [-0.0335193349815951]])

    # Call the compute_extrinsic function
    R, T, E, F = stereo_fisheye_calibrate(left_images, right_images, pattern_size, K_left, D_left, K_right, D_right)

    # Save the extrinsic parameters to a JSON file
    calibration_data = {
        'R': R.tolist(),  # Rotation matrix
        'T': T.tolist(),  # Translation vector
        'E': E.tolist(),  # Essential matrix
        'F': F.tolist()   # Fundamental matrix
    }

    # with open(f'{args.output_file}.json', 'w') as json_file:
    with open(f'{output_file}.json', 'w') as json_file:
        json.dump(calibration_data, json_file, indent=4)

    # print(f'Stereo extrinsic parameters saved to {args.output_file}.json')
    print(f'Stereo extrinsic parameters saved to {output_file}.json')


if __name__ == "__main__":
    main()
