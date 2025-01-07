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
    while True:
        frame = camera.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            #cv2.imwrite(path_, frame)
            break
    return frame

def write_image(img, path):
    cv2.imwrite(path, img)

if __name__ == "__main__":
    camera = format_camera()
    path = dirname(getcwd())
    for i in range(1):
        picture = make_picture(camera)
        path_ = join(path, f"JustDance_ComputerVision-1/Patterns/test2.png")
        write_image(picture, path_)
        print(f"Done {i}")
    print("Making photos endeded")
