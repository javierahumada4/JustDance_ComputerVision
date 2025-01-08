from Shi_tomasi import shi_tomasi_corner_detection
from picture import format_camera
import cv2
from time import sleep
from create_pasword import read_password
from state_machine import SecurityStateMachine

def main():
    camera = format_camera()
    max_corners, quality, min_distance, corner_color, radius = 7, 0.2, 7, (255, 0, 255), 5
    password = read_password()
    state_machine = SecurityStateMachine(password)
    frame_result = 0

    while True:
        frame = camera.capture_array()
        frame_corners, corners = shi_tomasi_corner_detection(frame, max_corners, quality, min_distance, corner_color, radius)

        if cv2.waitKey(1) == ord('q'):
            print("Next")
            frame_result = state_machine.process_corners(corners)
            print(frame_result)
        final_frame, result = draw_result(frame_corners, frame_result)
        cv2.imshow("picam", final_frame)
        if result == True and cv2.waitKey(1) == ord('f'):
            print("Access Granted!")
            break
    cv2.destroyAllWindows()

def draw_result(frame, result):
    """
    Draws an appropriate message and symbol on the given frame based on the result.

    :param frame: The image frame to draw on.
    :param result: The result code (-1, 0, 1, or 2).
    :return: True if the result is 2 (indicating completion), False otherwise.
    """
    h, w, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (0, 0, 0)

    if result == -1:
        # Draw a red 'X' in the corner
        color = (0, 0, 255)  # Red
        cv2.line(frame, (20, 20), (80, 80), color, thickness)
        cv2.line(frame, (80, 20), (20, 80), color, thickness)
        # Display error message
        cv2.putText(frame, "ERROR: TRY AGAIN", (50, h - 50), font, font_scale, color, thickness)

    elif result == 0:
        # Display "NEXT"
        color = (255, 255, 0)  # Cyan
        cv2.putText(frame, "Press q for next frame", (50, h - 50), font, font_scale, color, thickness)

    elif result == 1:
        # Draw a green tick in the corner
        color = (0, 255, 0)  # Green
        cv2.line(frame, (20, 50), (50, 80), color, thickness)
        cv2.line(frame, (50, 80), (80, 20), color, thickness)
        # Display success message
        cv2.putText(frame, "CORRECT", (50, h - 50), font, font_scale, color, thickness)

    elif result == 2:
        color = (0, 255, 0)  # Green
        cv2.putText(frame, "ACCESS GRANTED Press f to continue", (50, h - 50), font, font_scale, color, thickness)
        return frame, True

    return frame, False


if __name__ == "__main__":
    main()