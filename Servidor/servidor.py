# server.py
import socket
import struct
import os

import cv2
import time

import moviepy.editor as mp
 

#global variables
numSlaves = 0



def receive_file_size(sck: socket.socket):
    # Esta función se asegura de que se reciban los bytes
    # que indican el tamaño del archivo que será enviado,
    # que es codificado por el cliente vía struct.pack(),
    # función la cual genera una secuencia de bytes que
    # representan el tamaño del archivo.
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(sck: socket.socket, filename):
    # Leer primero del socket la cantidad de 
    # bytes que se recibirán del archivo.
    filesize = receive_file_size(sck)

    # Abrir un nuevo archivo en donde guardar
    # los datos recibidos.
    with open(filename, "wb") as f:

        received_bytes = 0
        # Recibir los datos del archivo en bloques de
        # 1024 bytes hasta llegar a la cantidad de
        # bytes total informada por el cliente.

        while received_bytes < filesize:

            chunk = sck.recv(1024)

            if chunk:

                f.write(chunk)

                received_bytes += len(chunk)

def send_file(sck: socket.socket, filename):
    # Obtener el tamaño del archivo a enviar.
    filesize = os.path.getsize(filename)
    # Informar primero al servidor la cantidad
    # de bytes que serán enviados.
    sck.sendall(struct.pack("<Q", filesize))
    # Enviar el archivo en bloques de 1024 bytes.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)



with socket.create_server(("localhost", 6190)) as server:
    print("Esperando al cliente...")
    conn, address = server.accept()
    print(f"{address[0]}:{address[1]} conectado.")
    print("Recibiendo archivo...")
    receive_file(conn, "dukibn.mp4")
    print("Archivo recibido.")


    send_file(conn,"dukibn.mp4")
    print("Archivo enviado al cliente")
    print("Conexión cerrada.")


#corta el video en clipas para los slaves
def cliping(video_location, num_clips):
    # Load the video clip
    clip = mp.VideoFileClip(video_location)
    cap = cv2.VideoCapture('dukibn.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    


    total_duration = clip.duration  # Duración total del video en segundos
    print ("duracion",total_duration)

    duration_per_clip = total_duration / num_clips  # Duración por cada clip
    print ("\nduration_per_clip ",duration_per_clip)
    
    clips = []  # Almacena los nombres de los clips generados
    
    # Dividir el video en el número de clips especificado
    for i in range(num_clips):

        start_time = i * duration_per_clip
        print ("start_time ",start_time)

        end_time = start_time + duration_per_clip
        print ("end_time ",end_time)

        print ("fps ",fps)
        
        # Nombre del clip basado en su número de orden
        clip_name = f"clip_{i + 1}.mp4"
        
        # Llamar a la función cut_video() para cortar cada sección del video
        cut_video(video_location, start_time, end_time, clip_name,fps)
        
        clips.append(clip_name)  # Agregar el nombre del clip a la lista de clips generados
    
    return clips


def cut_video(videoLocation, start_time, end_time, clipName, fps):

    # Load the video clip
    clip = mp.VideoFileClip(videoLocation)
    
    
    # Create a cropped subclip  
    cropped_clip = clip.subclip(start_time, end_time)

    # Create VideoWriter object to save the modified frames
    cropped_clip.write_videofile(clipName, codec='libx264', fps=cropped_clip.fps)
    

    return clipName



#juntar clips para hacer video procesado
def merge_video(Clips):
    #obtenemos todos los clips

    #los juntamos de acuerdo a el orden de los mismos

    #guardamos en una direccion
    videoMerged = ""

    return videoMerged

#def server_listen( ):
    #escucha para ver que recibe 

    #si recibe un usuario hace le isguiente

    #si recibe un slave hace lo siuguiente

    #si recibe un clip hace lo siguiente







