import socket
import math

def handle_client(socket_user):
    # Получаем данные от клиента
    user_data = socket_user.recv(1024).decode('utf-8')

    # Ожидаем, что клиент передаст два значения
    try:
        a, b = map(float, user_data.split())
        # Вычисляем гипотенузу по теореме Пифагора
        result = math.sqrt(a**2 + b**2)
        socket_user.send(f"Гипотенуза: {result}".encode('utf-8'))
    except ValueError:
        socket_user.send("Try another data".encode())

    socket_user.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8090))  
    server.listen(5)

    while True:
        socket_user, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        handle_client(socket_user)

if __name__ == "__main__":
    start_server()