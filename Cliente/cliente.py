import socket
import struct
import os

class VideoClient:
    def __init__(self, server_host, server_port, video_path):
        self.server_host = server_host
        self.server_port = server_port
        self.video_path = video_path

    def send_video(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_host, self.server_port))

            # Enviar el tamaño del archivo
            filesize = os.path.getsize(self.video_path)
            sock.sendall(struct.pack('Q', filesize))

            # Enviar el archivo
            with open(self.video_path, 'rb') as f:
                while read_bytes := f.read(4096):
                    sock.sendall(read_bytes)

            print("Video enviado. Esperando el video procesado...")

            # Recibir el video procesado
            processed_video_path = 'processed_video.mp4'
            self.receive_file(sock, processed_video_path)
            print(f"Video procesado recibido y guardado como {processed_video_path}")

    def receive_file(self, sock, file_path):
        # Recibir el tamaño del archivo
        file_size_data = sock.recv(8)
        file_size = struct.unpack('Q', file_size_data)[0]

        # Recibir y guardar el archivo
        with open(file_path, 'wb') as f:
            remaining = file_size
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = sock.recv(chunk_size)
                if not chunk: break
                f.write(chunk)
                remaining -= len(chunk)

if __name__ == "__main__":
    server_host = 'localhost'  # Asegúrate de cambiar esto por la dirección real del servidor
    server_port = 6190         # El puerto en el que está escuchando el servidor
    video_path = 'Cliente\machapan.mp4'  # La ruta del video a enviar

    client = VideoClient(server_host, server_port, video_path)
    client.send_video()