import cv2
import numpy as np
from os import getcwd
from os.path import dirname, join
import copy

def Calibrate(imgs):
    # Find corners with cv2.findChessboardCorners()
    corners =  [cv2.findChessboardCorners(img, (7, 7)) for img in imgs]
    valid_imgs = [img for img, corner in zip(imgs, corners) if corner[0]]
    
    imgs_gray = [cv2.cvtColor(valid_imgs[i], cv2.COLOR_RGB2GRAY) for i in range(len(valid_imgs))]
    valid_corners = [corners[i][1] for i in range(len(corners)) if corners[i][0]]
    corners_copy = copy.deepcopy(valid_corners)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01) # EPS + MAX_ITER, max 30 iterations, 0.01 accuracy(epsilon)
    corners_refined = [cv2.cornerSubPix(i, cor, (7, 7), (-1, -1), criteria) for i, cor in zip(imgs_gray, corners_copy)]
    
    imgs_with_corners = [cv2.drawChessboardCorners(valid_imgs[i], (7, 7), corners_refined[i], True) for i in range(len(valid_imgs))]
    for i in range(len(imgs_with_corners)):
        show_image(imgs_with_corners[i])
    
    chessboard_points = [get_chessboard_points((7,7), 30, 30) for i in range(len(valid_imgs))]
    valid_corners = np.asarray(valid_corners, dtype=np.float32)
    
    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(chessboard_points, valid_corners, imgs_gray[0].shape[::-1], None, None)

    # Obtain extrinsics
    extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))
    
    # Print outputs
    print("Intrinsics:\n", intrinsics)
    print("Distortion coefficients:\n", dist_coeffs)
    print("Root mean squared reprojection error:\n", rms)
    print("Extrinsics:\n", extrinsics)

def get_chessboard_points(chessboard_shape, dx, dy):
    objp = np.zeros((chessboard_shape[0] * chessboard_shape[1], 3), np.float32)

    objp[:, :2] = np.mgrid[0:chessboard_shape[0], 0:chessboard_shape[1]].T.reshape(-1, 2)
    objp[:, 0] *= dx
    objp[:, 1] *= dy
    return np.array(objp)

def show_image(img):
    cv2.imshow(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def write_image(img, path):
    cv2.imwrite(path, img)

def load_image(filename: list) -> list:
    return cv2.imread(filename)

if __name__ == "__main__":
    path = dirname(getcwd())
    path_ = join(path, f"JustDance_ComputerVision-1/chess")
    images = []
    for i in range(30):
        images.append(load_image(f"{path_}{i}.png"))

    Calibrate(images)
