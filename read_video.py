import cv2
from time import sleep

def open_video(path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
    
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow("Video", frame)
    cap.release()
    cv2.destroyAllWindows()

def live_video(camera, fps):
    while True:
        frame = camera.capture_array()
        cv2.imshow("picam", frame)
        sleep(1//fps)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
