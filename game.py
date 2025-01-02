import cv2
from picamera2 import Picamera2
import numpy as np

def stream_video():
    # Rango de colores de los "mandos"
    light_orange = (10, 25, 60)
    dark_orange = (35, 180, 215)
    
    # Lista para almacenar las posiciones actuales de los mandos
    detected_positions = [None, None]
    
    # Posición de ejemplo para demostrar el Just Dance
    ideal_positions = [
    (300, 200),  # Posición ideal para el mando 1
    (600, 200),  # Posición ideal para el mando 2
    ]

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
        # img_segmented = cv2.bitwise_and(frame, frame, mask=img_mask) # ESTA LINEA NO ES NECESARIA, PODEMOS USAR LA MASCARA DIRECTAMENTE PARA ENCONTRAR LOS CONTORNOS
        
        # Encuentra contornos en la máscara
        contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_boxes = []
        new_positions = []
        for contour in contours:
            if cv2.contourArea(contour) > 5000:  # Filtra por área mínima
                x, y, w, h = cv2.boundingRect(contour)
                detected_boxes.append((x, y, x + w, y + h))
                new_positions.append((x + w // 2, y + h // 2))
                
        # Dibuja las cajas alrededor de los objetos
        for box in detected_boxes:
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
        # Dibuja las posiciones ideales en la pantalla (usando círculos rojos)
        for ideal_pos in ideal_positions:
            cv2.circle(frame, ideal_pos, 10, (0, 0, 255), -1)  # Dibuja un círculo rojo en la posición ideal
            cv2.putText(frame, f"Ideal", (ideal_pos[0] + 15, ideal_pos[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
        # Compara las posiciones detectadas con las posiciones ideales
        if len(new_positions) == 2:
            detected_positions = new_positions
        for i, detected_pos in enumerate(detected_positions):
            if detected_pos is not None:
                ideal_pos = ideal_positions[i]
                distance = np.linalg.norm(np.array(detected_pos) - np.array(ideal_pos))

                # Si la distancia entre la posición detectada y la ideal es pequeña, mostramos por pantalla que es correcto
                if distance < 250: 
                    cv2.putText(frame, f"Mando {i+1}: Correcto", (10, 30 * (i+1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, f"Mando {i+1}: Incorrecto", (10, 30 * (i+1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()