# server.py
import socket
import struct
import os

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
def cut_video(Filename ):
    #obtenemos el archivo de video

    #ejecutamos la funcion para cortar el video

    #la cantidad de clips depende de la cantidad de slaves

    #arreglo para guardar los clips
    clips = []
    #
     
    #

    return clips

#juntar clips para hacer video procesado
def merge_video(Clips):
    #obtenemos todos los clips

    #los juntamos de acuerdo a el orden de los mismos

    #guardamos en una direccion
    videoMerged = ""

    return videoMerged

def server_listen( ):
    #escucha para ver que recibe 

    #si recibe un usuario hace le isguiente

    #si recibe un slave hace lo siuguiente

    #si recibe un clip hace lo siguiente


    return null

