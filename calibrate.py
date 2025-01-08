import cv2
import numpy as np
from os import getcwd
from os.path import dirname, join
import copy
from utils import write_image

def load_images(filenames: list) -> list:
    """
    Loads images from a list of filenames.

    Args:
        filenames (list): A list of file paths to the images.

    Returns:
        list: A list of loaded images.
    """
    return [cv2.imread(filename) for filename in filenames]

def get_paths(path: str, n: int, format: str) -> list:
    """
    Generates a list of file paths with a specific format.

    Args:
        path (str): The directory path.
        n (int): The number of file paths to generate.
        format (str): The base name format for the files.

    Returns:
        list: A list of file paths.
    """
    return [join(path, f"{format}{i}.png").replace("\\", "/") for i in range(n)]

def get_corners(imgs: list, grid: tuple) -> list:
    """
    Finds chessboard corners in a list of images.

    Args:
        imgs (list): A list of images.
        grid (tuple): The number of corners in the chessboard pattern (rows, columns).

    Returns:
        list: A list of tuples where each tuple contains a success flag and corners found.
    """
    return [cv2.findChessboardCorners(img, grid) for img in imgs]

def get_valid(imgs: list, grid: tuple) -> list:
    """
    Filters images and corners that have valid chessboard corners detected.

    Args:
        imgs (list): A list of images.
        grid (tuple): The chessboard grid dimensions (rows, columns).

    Returns:
        list: A tuple containing lists of valid corners and valid images.
    """
    corners = get_corners(imgs, grid)
    return [corners[i][1] for i in range(len(corners)) if corners[i][0]], [imgs[i] for i in range(len(imgs)) if corners[i][0]]

def get_refined_corners(corners: list, criteria: tuple, imgs_gray: list, grid: tuple) -> list:
    """
    Refines the detected chessboard corners in grayscale images.

    Args:
        corners (list): A list of initial corner detections.
        criteria (tuple): The termination criteria for corner refinement.
        imgs_gray (list): A list of grayscale images.
        grid (tuple): The chessboard grid dimensions (rows, columns).

    Returns:
        list: A list of refined corner positions.
    """
    corners_copy = copy.deepcopy(corners)
    return [cv2.cornerSubPix(imgs_gray[i], corner, grid, (-1, -1), criteria) for i, corner in enumerate(corners_copy)]

def get_chessboard_points(chessboard_shape, dx, dy):
    """
    Generates 3D points for a chessboard pattern.

    Args:
        chessboard_shape (tuple): The number of inner corners per a chessboard row and column (rows, columns).
        dx (float): The distance between points in the x-direction.
        dy (float): The distance between points in the y-direction.

    Returns:
        numpy.ndarray: The 3D points in real-world space.
    """
    objp = np.zeros((chessboard_shape[0] * chessboard_shape[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_shape[0], 0:chessboard_shape[1]].T.reshape(-1, 2)
    objp[:, 0] *= dx
    objp[:, 1] *= dy
    return np.array(objp)

def draw_chessboard_corners(imgs, corners, grid):
    """
    Draws detected chessboard corners on the images.

    Args:
        imgs (list): A list of images.
        corners (list): A list of detected corners.
        grid (tuple): The chessboard grid dimensions (rows, columns).

    Returns:
        list: A list of images with drawn chessboard corners.
    """
    return [cv2.drawChessboardCorners(imgs[i], grid, corners[i], True) for i in range(len(imgs))]

def calibrate_camera(chessboard_points, valid_corners, imgs_gray):
    """
    Calibrates the camera using detected corners and chessboard points.

    Args:
        chessboard_points (list): 3D points of the chessboard corners.
        valid_corners (list): 2D points of detected corners in the image plane.
        imgs_gray (list): A list of grayscale images.

    Returns:
        tuple: The camera matrix, distortion coefficients, rotation vectors, and translation vectors.
    """
    return cv2.calibrateCamera(chessboard_points, valid_corners, imgs_gray[0].shape[::-1], None, None)

def get_extrinsics(rvecs, tvecs):
    """
    Computes the extrinsic parameters (rotation and translation) for each image.

    Args:
        rvecs (list): Rotation vectors from camera calibration.
        tvecs (list): Translation vectors from camera calibration.

    Returns:
        list: A list of extrinsic matrices for each image.
    """
    return list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))


if __name__ == "__main__":
    path = dirname(getcwd())
    path_ = join(path, r"JustDance_ComputerVision-1")
    paths = get_paths(path_, 30, "Calibration/chess")
    images = load_images(paths)
    grid = (7, 7)
    valid_corners, valid_imgs = get_valid(images, grid)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
    imgs_gray = [cv2.cvtColor(valid_imgs[i], cv2.COLOR_RGB2GRAY) for i in range(len(valid_imgs))]

    refined_corners = get_refined_corners(valid_corners, criteria, imgs_gray, grid)
    chessboard_points = [get_chessboard_points(grid, 30, 30) for i in range(len(valid_imgs))]
    chessboard_imgs = draw_chessboard_corners(valid_imgs, refined_corners, grid)
    for i in range(len(chessboard_imgs)):
        write_image(chessboard_imgs[i], join(path_, f"calibration/chessboard{i}.png"))

    rms, intrinsics, dist_coeffs, rvecs, tvecs = calibrate_camera(chessboard_points, refined_corners, imgs_gray)
    extrinsics = get_extrinsics(rvecs, tvecs)

    print("Intrinsics:\n", intrinsics)
    print("Distortion coefficients:\n", dist_coeffs)
    print("Root mean squared reprojection error:\n", rms)
