import numpy as np
import cv2
import time

# Capturamos el vídeo
cap = cv2.VideoCapture(r'C:/Users/jquin/PersonalWorkSpace/SistemasDistribuidos/Proyecto3/Cluster/Esclavo/machapan.mp4')
# Llamada al método
fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

# Obtén las dimensiones del video original
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Configura el escritor de video para la sustracción de fondo
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_bgsub = cv2.VideoWriter('sustraccion_fondo_output.avi', fourcc, 20.0, (width, height), isColor=False)

i = 1 
while(1):
    # Leemos el siguiente frame
    i += 1
    ret, frame = cap.read()

    # Si hemos llegado al final del vídeo salimos
    if not ret:
        break

    # Aplicamos el algoritmo de sustracción de fondo
    fgmask = fgbg.apply(frame)

    # Escribir el frame de sustracción de fondo en el video de salida
    out_bgsub.write(fgmask)

    # Mostramos las capturas
    cv2.imshow('Camara', frame)
    cv2.imshow('Sustraccion de Fondo', fgmask)

    # Sentencias para salir, pulsa 's' y sale
    k = cv2.waitKey(30) & 0xff
    if k == ord("s"):
        break
    elif k == ord("p"):
        time.sleep(10)

# Liberamos la cámara, el escritor de video y cerramos todas las ventanas
print("no de cuadros: ", i)
cap.release()
out_bgsub.release()
cv2.destroyAllWindows()
