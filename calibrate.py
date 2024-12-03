import cv2
import numpy as np
from os import getcwd
from os.path import dirname, join
import copy

def show_image(img):
    cv2.imshow(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def write_image(img, path):
    cv2.imwrite(path, img)

def load_images(filenames: list) -> list:
    return [cv2.imread(filename) for filename in filenames]

def get_paths(path: str, n: int, format: str ) -> list:
    return [join(path, f"{format}{i}.png").replace("\\", "/") for i in range(n)]

def get_corners(imgs: list, grid: tuple) -> list:
    return [cv2.findChessboardCorners(img, grid) for img in imgs]

def get_valid(imgs: list, grid: tuple) -> list:
    corners = get_corners(imgs, grid)
    return [corners[i][1] for i in range(len(corners)) if corners[i][0]], [imgs[i] for i in range(len(imgs)) if corners[i][0]]

def get_refined_corners(corners: list, criteria: tuple, imgs_gray: list, grid: tuple) -> list:
    corners_copy = copy.deepcopy(corners)
    return [cv2.cornerSubPix(imgs_gray[i], corner, grid, (-1, -1), criteria) for i, corner in enumerate(corners_copy)]

def get_chessboard_points(chessboard_shape, dx, dy):
    objp = np.zeros((chessboard_shape[0] * chessboard_shape[1], 3), np.float32)

    objp[:, :2] = np.mgrid[0:chessboard_shape[0], 0:chessboard_shape[1]].T.reshape(-1, 2)
    objp[:, 0] *= dx
    objp[:, 1] *= dy
    return np.array(objp)

def draw_chessboard_corners(imgs, corners, grid):
    return [cv2.drawChessboardCorners(imgs[i], grid, corners[i], True) for i in range(len(imgs))]

def calibrate_camera(chessboard_points, valid_corners, imgs_gray):
    return cv2.calibrateCamera(chessboard_points, valid_corners, imgs_gray[0].shape[::-1], None, None)

def get_extrinsics(rvecs, tvecs):
    return list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

def calibration():
    pass

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
