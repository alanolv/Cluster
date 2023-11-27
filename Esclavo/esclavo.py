# Importación de librerías
import numpy as np
import cv2
import time
 
# Capturamos el vídeo
cap = cv2.VideoCapture(r'C:/Users/jquin/PersonalWorkSpace/SistemasDistribuidos/Proyecto3/Cluster/Esclavo/machapan.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Llamada al método
fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)
output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))
i=1
while(1):
	# Leemos el siguiente frame
	i+=1
	ret, frame = cap.read()
 
	# Si hemos llegado al final del vídeo salimos
	if not ret:
		break
 
	# Aplicamos el algoritmo
	fgmask = fgbg.apply(frame)
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
	edges = cv2.Canny(img_gray,100,200)

	'''
	# Copiamos el umbral para detectar los contornos
	contornosimg = fgmask.copy()
	# Buscamos contorno en la imagen
	contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 	
	# Recorremos todos los contornos encontrados
	for c in contornos:
		# Eliminamos los contornos más pequeños
		if cv2.contourArea(c) < 500:
			continue
 
		# Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
		(x, y, w, h) = cv2.boundingRect(c)
		# Dibujamos el rectángulo del bounds
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	'''
	# Mostramos las capturas

	#cv2.imshow('Camara',frame)
	#cv2.imshow('Umbral',fgmask)
	#cv2.imshow('gris',edges)
 
	# Sentencias para salir, pulsa 's' y sale
	k = cv2.waitKey(30) & 0xff
	if k == ord("s"):
		break
	elif k == ord("p"):
		time.sleep(10)
 
# Liberamos la cámara y cerramos todas las ventanas
print("no de cuadros: ",i)
cap.release()
output_video.release()
cv2.destroyAllWindows()
#cv2.destroyAllWindows()
