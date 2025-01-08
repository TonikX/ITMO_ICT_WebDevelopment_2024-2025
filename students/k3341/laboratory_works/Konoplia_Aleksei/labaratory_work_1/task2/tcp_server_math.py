import socket
import threading
import math

def tcp_server_math():
    def handle_client(client_socket):
        try:
            operation = client_socket.recv(1024).decode()
            if operation == "1":  # Теорема Пифагора
                a = float(client_socket.recv(1024).decode())
                b = float(client_socket.recv(1024).decode())
                result = math.sqrt(a ** 2 + b ** 2)
                client_socket.sendall(str(result).encode())
            elif operation == "2":  # Квадратное уравнение
                a = float(client_socket.recv(1024).decode())
                b = float(client_socket.recv(1024).decode())
                c = float(client_socket.recv(1024).decode())
                discriminant = b ** 2 - 4 * a * c
                if discriminant >= 0:
                    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                    result = f"Корни: {root1}, {root2}"
                else:
                    result = "Нет действительных корней"
                client_socket.sendall(result.encode())
        finally:
            client_socket.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 23456))
    server_socket.listen(5)
    print("TCP сервер запущен на порту 23456")

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    tcp_server_math()