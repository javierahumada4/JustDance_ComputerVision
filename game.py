import cv2
from picamera2 import Picamera2

def stream_video():
    # Define orange color range
    light_orange = (10, 25, 60)
    dark_orange = (35, 180, 215)
    
    # Lista para almacenar trackers y cajas correspondientes
    trackers = [None, None]
    tracker_boxes = [None, None]

    # Inicializar la cámara
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
        # img_segmented = cv2.bitwise_and(frame, frame, mask=img_mask) ESTA LINEA NO ES NECESARIA, PODEMOS USAR LA MASCARA DIRECTAMENTE PARA ENCONTRAR LOS CONTORNOS
        
        # Encuentra contornos en la máscara
        contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Dibuja rectángulos alrededor de los objetos segmentados
        detected_boxes = []
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filtra por área mínima
                x, y, w, h = cv2.boundingRect(contour)
                detected_boxes.append((x, y, x + w, y + h))

        # Actualiza los trackers existentes
        for i in range(2):
            if trackers[i] is not None:
                success, new_box = trackers[i].update(frame)
                if success:
                    tracker_boxes[i] = tuple(map(int, new_box))
                    # Dibuja la caja actualizada
                    x, y, w, h = map(int, new_box)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    # Si falla el tracker, lo reiniciamos a None
                    trackers[i] = None
                    tracker_boxes[i] = None

        # Asigna nuevos trackers a objetos detectados que no están siendo rastreados
        for box in detected_boxes:
            # Verifica si el objeto ya está siendo rastreado
            already_tracked = any(
                tracker_box is not None and
                abs(box[0] - tracker_box[0]) < 50 and
                abs(box[1] - tracker_box[1]) < 50
                for tracker_box in tracker_boxes
            )

            if not already_tracked:
                # Busca un tracker vacío para asignar
                for i in range(2):
                    if trackers[i] is None:
                        trackers[i] = cv2.TrackerCSRT_create()
                        trackers[i].init(frame, tuple(box))
                        tracker_boxes[i] = box
                        break


        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()