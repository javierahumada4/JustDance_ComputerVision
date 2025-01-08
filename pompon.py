import cv2
from utils import get_hsv_color_ranges
from os import getcwd
from os.path import dirname, join

path = dirname(getcwd())
path_ = join(path, f"JustDance_ComputerVision-1/pompon.png")
img = cv2.imread(path_)
get_hsv_color_ranges(img)