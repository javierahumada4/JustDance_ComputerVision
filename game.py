import cv2
from picamera2 import Picamera2

def stream_video():
    # Define orange color range
    light_orange = (10, 25, 60)
    dark_orange = (35, 180, 215)

    picam = Picamera2()
    picam.preview_configuration.main.size=(1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    while True:
        frame = picam.capture_array()

        # Change the image to a color space in which chroma and intensity are separate
        hsv_img = cv2.cvtColor(frame, code=cv2.COLOR_BGR2HSV) 
        # Compute a list that contains a mask (which should segment orange colors) for every image.
        img_mask = cv2.inRange(hsv_img, light_orange, dark_orange)
        # Compute a list that contains the result of multiplying the original image with its orange colors mask.
        img_segmented = cv2.bitwise_and(frame, frame, mask=img_mask)

        cv2.imshow("picam", img_segmented)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()