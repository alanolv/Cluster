import socket
import cv2
import struct
import os
import threading


class VideoServer:
    def __init__(self, host='192.168.210.195', port=6190):
        self.host = host
        self.port = port
        self.server_socket = None
        self.slave_sockets = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        
        self.connect_to_slaves()
        

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()
            
    def connect_to_slaves(self):
        slaves_info = [("192.168.210.129", 6203), ("192.168.210.179", 6203), ("192.168.210.63", 6207)]
        for slave_ip, slave_port in slaves_info:
            slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            slave_socket.connect((slave_ip, slave_port))
            self.slave_sockets.append(slave_socket)
            print(f"Connected to slave {slave_ip}:{slave_port}")
            
    def handle_client(self, conn, addr):
        print(f"Connection from {addr}")

        # Recibir el video del cliente y procesarlo en clips
        video_path = f"received_video_from_{addr[0]}.mp4"
        self.receive_file(conn, video_path)
        clips = self.process_video(video_path)

        # Asegurarse de que hay suficientes esclavos para los clips
        if len(clips) > len(self.slave_sockets):
            print("No hay suficientes servidores esclavos para procesar los clips")
            return

        # Enviar clips a los servidores esclavos y recibir los clips procesados
        threads = []
        processed_clips = []  # Lista para almacenar los caminos de los clips procesados

        for i, clip in enumerate(clips):
            processed_clip_path = f"processed_clip_{i+1}.mp4"
            processed_clips.append(processed_clip_path)  # Agregar el camino a la lista
            thread = threading.Thread(target=self.send_and_receive_from_slave, 
                                    args=(self.slave_sockets[i], clip, processed_clip_path, processed_clips))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        # Combinar los clips procesados en un solo video
        output_video_path = "final_output_video.mp4"
        self.combine_clips(processed_clips, output_video_path)
        print(f"Video final combinado guardado en {output_video_path}")
        self.send_file(conn, output_video_path)
        
        conn.close()
        print(f"Conexión con el cliente {addr} cerrada.")

    def receive_file(self, conn, file_path):
        # Paso 1: Recibir el tamaño del archivo
        file_size_data = conn.recv(8)
        if not file_size_data:
            raise ValueError("No se recibieron datos del tamaño del archivo")
        file_size = struct.unpack('Q', file_size_data)[0]

        # Paso 2: Recibir y guardar el archivo
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
    def process_video(self, video_path):
        # Abrir el video original
        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_per_clip = total_frames // 3

        clips = []
        for i in range(3):
            clip_path = f"clip_{i+1}.mp4"
            clips.append(clip_path)

            # Crear un nuevo archivo de video para cada clip
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = video.get(cv2.CAP_PROP_FPS)
            frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(clip_path, fourcc, fps, (frame_width, frame_height))

            # Escribir frames en el clip
            for _ in range(frames_per_clip):
                ret, frame = video.read()
                if not ret:
                    break
                out.write(frame)

            out.release()

        video.release()
        return clips
    
    def connect_and_send_to_slave(self, slave_ip, slave_port, clip_path, processed_clip_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((slave_ip, slave_port))
            self.send_file(sock, clip_path)
            print(f"Archivo {clip_path} enviado al esclavo {slave_ip}:{slave_port}")

            # Recibir el clip procesado del esclavo
            self.receive_file(sock, processed_clip_path)
            
    def send_and_receive_from_slave(self, slave_socket, clip_path, processed_clip_path, processed_clips):
        # Enviar el archivo al servidor esclavo usando la conexión existente
        self.send_file(slave_socket, clip_path)
        print(f"Archivo {clip_path} enviado al servidor esclavo")

        # Recibir el clip procesado del servidor esclavo
        self.receive_file(slave_socket, processed_clip_path)
       
            
    def combine_clips(self, clips, output_path):
        # Asegurarse de que cada clip se procesa una sola vez
        first_clip = cv2.VideoCapture(clips[0])
        fps = first_clip.get(cv2.CAP_PROP_FPS)
        frame_width = int(first_clip.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(first_clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
        first_clip.release()

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        for clip in clips:
            video = cv2.VideoCapture(clip)
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                out.write(frame)
            video.release()

        out.release()
    
    def send_file(self, conn, file_path):
        # Paso 1: Obtener y enviar el tamaño del archivo
        filesize = os.path.getsize(file_path)
        conn.sendall(struct.pack('Q', filesize))

        # Paso 2: Enviar el archivo
        with open(file_path, 'rb') as f:
            while read_bytes := f.read(4096):
                conn.sendall(read_bytes)
                
                
if __name__ == "__main__":
    server = VideoServer()
    server.start()

