import socket
import threading


def receive_messages(client_socket):
    """Функция для получения сообщений от сервера."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            break


def start_client():
    """Запуск клиента и подключение к серверу."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))

    name = input("Введите ваше имя: ")
    client_socket.send(name.encode())

    # Запускаем поток для получения сообщений от других клиентов
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Отправляем сообщения на сервер
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())

    client_socket.close()


if __name__ == "__main__":
    start_client()
