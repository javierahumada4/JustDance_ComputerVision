from picamera2 import Picamera2
import cv2
from os import getcwd
from os.path import dirname, join

def format_camera():
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    return picam

def make_picture(camera):
    picture = camera.capture_array()
    cv2.imshow("picam", picture)
    return picture

def write_image(img, path):
    cv2.imwrite(path, img)

if __name__ == "__main__":
    camera = format_camera()
    for i in range(10):
        path = join(dirname(getcwd()), "data")
        videopath = join(path, f"corners_{i}.png")
        write_image(make_picture(camera), path)
    print("Making photos endeded")
