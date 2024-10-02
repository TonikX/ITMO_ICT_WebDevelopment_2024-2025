import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 12345))

server_socket.listen(5)
print("Сервер запущен и ожидает подключения...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Клиент {client_address} подключен")

    data = client_socket.recv(1024).decode('utf-8')
    
    try:
        a, b = map(float, data.split())
        c = math.sqrt(a**2 + b**2)
        result = f"гипотенуза равна {c}"
    except ValueError:
        result = "Ошибка: введите два числа."

    client_socket.send(result.encode('utf-8'))
    
    client_socket.close()
