import socket
import threading

def receive_messages(client_socket):
    """
    Функция для получения сообщений от сервера.
    """
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

def start_client():
    """
    Запуск клиента.
    """
    # Создаем TCP-сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8888))

    # Получаем имя пользователя от пользователя и отправляем его на сервер
    username = input("Введите ваше имя: ")
    client_socket.send(username.encode())

    # Запускаем поток для получения сообщений от сервера
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Отправляем сообщение на сервер
        message = input()
        client_socket.send(message.encode())

if __name__ == '__main__':
    start_client()
