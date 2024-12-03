import numpy as np
import cv2
from os import getcwd
from os.path import dirname, join
import imageio
from typing import List
import glob
from calibrate import get_paths, load_images, write_image
from detect_shapes import is_square

def shi_tomasi_corner_detection(image: np.array, maxCorners: int, qualityLevel:float, minDistance: int, corner_color: tuple, radius: int):
    '''
    image - Input image
    maxCorners - Maximum number of corners to return. 
                 If there are more corners than are found, the strongest of them is returned. 
                 maxCorners <= 0 implies that no limit on the maximum is set and all detected corners are returned
    qualityLevel - Parameter characterizing the minimal accepted quality of image corners. 
                   The parameter value is multiplied by the best corner quality measure, which is the minimal eigenvalue or the Harris function response. 
                   The corners with the quality measure less than the product are rejected. 
                   For example, if the best corner has the quality measure = 1500, and the qualityLevel=0.01 , then all the corners with the quality measure less than 15 are rejected
    minDistance - Minimum possible Euclidean distance between the returned corners
    corner_color - Desired color to highlight corners in the original image
    radius - Desired radius (pixels) of the circle
    '''
    # TODO Input image to Tomasi corner detector should be grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Shi-Tomasi corner detection
    corners = cv2.goodFeaturesToTrack(
        gray, 
        maxCorners=maxCorners, 
        qualityLevel=qualityLevel, 
        minDistance=minDistance
    )
    
    # Ensure corner coordinates are integers
    corners = np.int0(corners)
    
    # Draw circles around each detected corner
    for corner in corners:
        x, y = corner.ravel()  # Flatten the coordinates
        cv2.circle(image, (x, y), radius, corner_color, -1)  # Draw filled circle
    
    return image, corners

def canny_line_detection(img, low_threshold, high_threshold):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge_img = cv2.Canny(gray_img, low_threshold, high_threshold)
    return edge_img

if __name__ == "__main__":
    path = dirname(getcwd())
    path_ = join(path, r"JustDance_ComputerVision-1")
    paths = get_paths(path_, 4, "Patterns/test")
    images = load_images(paths)
    max_corners, quality, min_distance, corner_color, radius = 4, 0.3, 7, (255, 0, 255), 5
    shi_tomasi_corners = [shi_tomasi_corner_detection(img, max_corners, quality, min_distance, corner_color, radius)[1] for img in images]
    #for i, image in enumerate(shi_tomasi_corners):
    #    write_image(image, join(path_, f"Patterns/shi{i}.png"))
    low, high = 50, 120
    canny_images = [canny_line_detection(img, low, high) for img in images]
    #for i, image in enumerate(canny_images):
     #   write_image(image, join(path_, f"Patterns/canny{i}.png"))
    for i in range(len(canny_images)):
        shi_corner = shi_tomasi_corners[i]
        canny = canny_images[i]
        for corner in shi_corner:
            x, y = corner.ravel()  # Flatten the coordinates
            cv2.circle(canny, (x, y), radius, corner_color, -1)  # Draw filled circle
        write_image(canny, join(path_, f"Patterns/Total{i}.png"))
    
    for corner in shi_tomasi_corners:
        print(corner)
        tolerance = 50
        print(is_square(corner))
