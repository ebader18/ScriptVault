# Example: python .\stereo_camera_projection.py --resolution 3280 2464 --fov 73 50 --baseline 60 --point 0 0 1000

import argparse
import numpy as np


def calculate_intrinsic_parameters(resolution, fov):
    """Calculate the intrinsic camera matrix based on the resolution and field of view."""
    width, height = resolution
    fov_x, fov_y = fov

    # Convert FOV from degrees to radians
    fov_x_rad = np.deg2rad(fov_x)
    fov_y_rad = np.deg2rad(fov_y)

    # Focal lengths in pixels
    fx = width / (2 * np.tan(fov_x_rad / 2))
    fy = height / (2 * np.tan(fov_y_rad / 2))

    # Principal point (assuming the center of the image)
    cx = width / 2
    cy = height / 2

    # Intrinsic matrix
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]])

    return K


def calculate_extrinsic_parameters(baseline):
    """Calculate the extrinsic camera matrices for two cameras."""
    # Assume the origin is at the midpoint between the two cameras
    # Camera 1: translated to the left by baseline/2
    T1 = np.array([[-baseline / 2, 0, 0]])
    # Camera 2: translated to the right by baseline/2
    T2 = np.array([[baseline / 2, 0, 0]])

    # Rotation matrices (identity since there is no rotation)
    R1 = np.eye(3)
    R2 = np.eye(3)

    # Extrinsic matrices for each camera
    extrinsic1 = np.hstack((R1, T1.T))
    extrinsic2 = np.hstack((R2, T2.T))

    return extrinsic1, extrinsic2


def project_point(K, extrinsic, point_3d):
    """Project a 3D point into the 2D space of a camera."""
    # Convert the 3D point to homogeneous coordinates
    point_3d_h = np.append(point_3d, 1)

    # Project the 3D point using the extrinsic matrix
    camera_coords = extrinsic @ point_3d_h

    # Project to 2D using the intrinsic matrix
    pixel_coords_h = K @ camera_coords

    # Normalize homogeneous coordinates
    pixel_coords = pixel_coords_h[:2] / pixel_coords_h[2]

    return pixel_coords


def calculate_disparity(point_2d_cam1, point_2d_cam2):
    """Calculate the disparity between two projected 2D points."""
    return abs(point_2d_cam1[0] - point_2d_cam2[0])


def main():
    parser = argparse.ArgumentParser(description="Calculate camera parameters and project a 3D point.")
    parser.add_argument("--resolution", type=int, nargs=2, default=[3280, 2464], required=False, help="Camera resolution as width height in pixels.")
    parser.add_argument("--fov", type=float, nargs=2, default=[73.0, 50.0], required=False, help="Horizontal and vertical field of view in degrees.")
    parser.add_argument("--baseline", type=float, default=60.0, required=False, help="Baseline between the two cameras in mm.")
    parser.add_argument("--point", type=float, nargs=3, default=[0.0, 0.0, 1000.0], required=False, help="3D coordinate of the point in the global coordinate system in mm.")

    args = parser.parse_args()

    # Parse arguments
    resolution = tuple(args.resolution)
    fov = tuple(args.fov)
    baseline = args.baseline
    point_3d = np.array(args.point)

    # Calculate intrinsic parameters
    K = calculate_intrinsic_parameters(resolution, fov)
    print("Intrinsic Matrix (K):\n", K)

    # Calculate extrinsic parameters for both cameras
    extrinsic1, extrinsic2 = calculate_extrinsic_parameters(baseline)
    print("Extrinsic Matrix for Camera 1:\n", extrinsic1)
    print("Extrinsic Matrix for Camera 2:\n", extrinsic2)

    # Project the 3D point into the 2D space of both cameras
    point_2d_cam1 = project_point(K, extrinsic1, point_3d)
    point_2d_cam2 = project_point(K, extrinsic2, point_3d)

    print("2D projection in Camera 1:", point_2d_cam1)
    print("2D projection in Camera 2:", point_2d_cam2)

    # Calculate the disparity
    disparity = calculate_disparity(point_2d_cam1, point_2d_cam2)
    print("Disparity (in pixels):", disparity)


if __name__ == "__main__":
    main()
