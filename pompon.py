import os
import cv2
import imageio
import numpy as np
from typing import List
from utils import non_max_suppression, get_hsv_color_ranges
from os import getcwd
from os.path import dirname, join

# Complete the method, use every argument    
def show_image(img: np.array, title: str = "Image"):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

path = dirname(getcwd())
path_ = join(path, f"JustDance_ComputerVision-1/pompon.png")
img = cv2.imread(path)
get_hsv_color_ranges(img)