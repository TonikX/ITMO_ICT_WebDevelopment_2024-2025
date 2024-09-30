import socket
import math


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1) 

print("Сервер запущен и ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключен клиент с адресом: {addr}")

    data = conn.recv(1024).decode()
    if not data:
        break

    a, b = map(float, data.split(','))

    c = math.sqrt(a**2 + b**2)
    
    conn.send(str(c).encode())

    print(f"Вычисленная гипотенуза: {c}")

    conn.close()