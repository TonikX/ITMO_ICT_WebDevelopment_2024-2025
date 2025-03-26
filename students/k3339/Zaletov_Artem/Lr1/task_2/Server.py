import socket
import math
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            a, b = map(float, data.split(','))
            c = math.sqrt(a ** 2 + b ** 2)
            conn.sendall(str(c).encode())
        except Exception as e:
            conn.sendall(f"Ошибка: {str(e)}".encode())
        finally:
            conn.close()

if __name__ == '__main__':
    start_server()