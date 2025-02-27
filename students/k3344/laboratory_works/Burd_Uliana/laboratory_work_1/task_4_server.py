import socket
import threading

# Словарь для хранения клиентских соединений
clients = {}

def handle_client(client_socket, client_address):
    """
    Обработчик клиентского соединения.
    """
    # Получаем имя пользователя от клиента
    username = client_socket.recv(1024).decode()

    # Сохраняем клиентское соединение в словаре
    clients[username] = client_socket

    # Отправляем приветственное сообщение клиенту
    client_socket.send(f"Добро пожаловать, {username}!".encode())

    while True:
        # Получаем сообщение от клиента
        message = client_socket.recv(1024).decode()

        # Если клиент отключился, удаляем его соединение из словаря
        if not message:
            del clients[username]
            break

        # Отправляем сообщение всем остальным клиентам
        for name, socket in clients.items():
            if name != username:
                socket.send(f"{username}: {message}".encode())

    # Закрываем клиентское соединение
    client_socket.close()

def start_server():
    """
    Запуск сервера.
    """
    # Создаем TCP-сокет и связываем его с адресом 127.0.0.1:8888
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen()

    while True:
        # Принимаем новое клиентское соединение
        client_socket, client_address = server_socket.accept()

        # Запускаем обработчик клиентского соединения в отдельном потоке
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()
