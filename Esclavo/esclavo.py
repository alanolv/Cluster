import socket
import cv2
import struct
import numpy as np
import os


class VideoSlave:
    def __init__(self, host='localhost', port=6201):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            print(f"Slave listening on {self.host}:{self.port}")

            while True:
                conn, addr = sock.accept()
                print(f"Connection from {addr}")
                self.handle_connection(conn)

    def handle_connection(self, conn):
        # Recibir el clip de video
        video_path = "received_clip.mp4"
        self.receive_file(conn, video_path)

        # Procesar el clip de video
        processed_video_path = self.process_clip(video_path)

        # Enviar el clip procesado de vuelta al servidor central
        self.send_file(conn, processed_video_path)

        conn.close()
    
    def receive_file(self, conn, file_path):
        # Paso 1: Recibir el tamaño del archivo
        file_size_data = conn.recv(8)
        if not file_size_data:
            raise ValueError("No se recibieron datos del tamaño del archivo")
        file_size = struct.unpack('Q', file_size_data)[0]
        with open(file_path, 'wb') as f:
            remaining = file_size
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = conn.recv(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)
            if remaining != 0:
                raise IOError("No se recibieron todos los datos del archivo")

	
    def process_clip(self, video_path):
        # Abrir el video original
        video = cv2.VideoCapture(video_path)
        processed_video_path = "processed_" + video_path
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (frame_width, frame_height))

        # Procesar cada frame para convertirlo a bordes
        while True:
            ret, frame = video.read()
            if not ret:
                break
            edges = cv2.Canny(frame, 100, 200)  # Convertir a bordes
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Convertir a BGR para el video
            out.write(edges_colored)

        video.release()
        out.release()
        return processed_video_path

    def send_file(self, conn, file_path):
        filesize = os.path.getsize(file_path)
        conn.sendall(struct.pack('Q', filesize))
        
        with open(file_path, 'rb') as f:
            while read_bytes := f.read(4096):
                conn.sendall(read_bytes)

if __name__ == "__main__":
    slave = VideoSlave()
    slave.start()