import socket
import math


def pythagoras(a, b):
    return math.sqrt(a**2 + b**2)

# Создаем TCP-сервер
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Сервер запущен и ожидает подключения...")

while True:
    # Принимаем соединение и получаем данные от клиента
    client_socket, addr = server_socket.accept()
    print(f"Клиент {addr} подключился.")

    data = client_socket.recv(1024).decode()
    a, b = map(float, data.split(','))

    # Вычисляем гипотенузу
    result = pythagoras(a, b)

    # Отправляем результат клиенту
    client_socket.send(f"Гипотенуза: {result:.2f}".encode())

    # Закрываем соединение с клиентом
    client_socket.close()

