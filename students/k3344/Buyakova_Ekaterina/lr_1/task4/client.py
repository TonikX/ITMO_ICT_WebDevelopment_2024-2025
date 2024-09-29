import socket
import threading
import sys

# Параметры сервера
HOST = 'localhost'
PORT = 8080


# Функция для приема сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            # Получаем сообщения от сервера
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f'\r{message}\nYou: ', end='')
        except:
            # Закрываем соединение, если произошла ошибка
            print("Error when receiving message.")
            client_socket.close()
            break


# Функция для отправки сообщений серверу
def send_messages(client_socket):
    while True:
        message = input("You: ")  # Получаем сообщение от пользователя

        # Отправляем сообщение серверу
        client_socket.send(message.encode('utf-8'))

        # Очищаем последнюю строку (написанное сообщение)
        sys.stdout.write("\033[F")  # Перемещаем курсор на строку вверх
        sys.stdout.write("\033[K")  # Очищаем строку


# Подключение к серверу
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connection to the server is successful.")

    # Создаем поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Отправляем сообщения серверу
    send_messages(client_socket)


# Запуск клиента
start_client()
