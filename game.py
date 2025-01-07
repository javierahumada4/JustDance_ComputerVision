import cv2
from picamera2 import Picamera2
import numpy as np
import time

def stream_video():
    # Rango de colores de los "mandos"
    light_orange = (10, 25, 60)
    dark_orange = (35, 180, 215)
    
    # Lista para almacenar las posiciones actuales de los mandos
    detected_positions = [None, None]
    
    # Posición de ejemplo para demostrar el Just Dance
    ideal_positions = [
    (300, 200),  # Posición ideal para el mando 1
    (900, 200),  # Posición ideal para el mando 2
    ]

    # Inicializar la cámara
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280, 720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    
    # Configurar el VideoWriter para guardar el video
    frame_width = 1280
    frame_height = 720
    fps = 10  # Estimación inicial; puede ajustarse más tarde si se mide programáticamente
    video_writer = cv2.VideoWriter('outputvideo.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

    # Variables para calcular FPS
    prev_time = time.time()

    while True:
        frame = picam.capture_array()
        
        # Calcular FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

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

        # Mostrar FPS en el cuadro
        cv2.putText(frame, f"FPS: {int(fps)}", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Escribir el cuadro en el archivo de video
        video_writer.write(frame)

        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar los recursos
    video_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()