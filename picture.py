import cv2
from os import getcwd
from os.path import dirname, join
from utils import format_camera

def make_picture(camera):
    while True:
        frame = camera.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    return frame

def write_image(img, path):
    cv2.imwrite(path, img)

if __name__ == "__main__":
    camera = format_camera()
    path = dirname(getcwd())
    for i in range(4):
        picture = make_picture(camera)
        path_ = join(path, f"JustDance_ComputerVision-1/Patterns/test{i}.png")
        write_image(picture, path_)
        print(f"Done {i}")
    print("Making photos endeded")
