from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Создаем сокет
client_socket = socket(AF_INET, SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Получаем приглашение для ввода никнейма
nickname_prompt = client_socket.recv(1024).decode()
nickname = input(nickname_prompt)
client_socket.send(nickname.encode())


def receive_messages() -> None:
    """Получение сообщений от сервера"""
    while True:
        try:
            # Получаем сообщение от сервера
            receive_message = client_socket.recv(1024).decode()
            if receive_message:
                print(receive_message)
            else:
                print("Соединение с сервером разорвано")
                break
        except:
            print("Ошибка получения сообщений")
            break


# Запускаем поток для получения сообщений
receive_thread = Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

print("Подключение установлено! Начинайте общаться (для выхода введите '/quit'):")

# Основной цикл для отправки сообщений
while True:
    message = input()
    if message.lower() == '/quit':
        break
    if message.strip():  # Не отправляем пустые сообщения
        full_message = f"{nickname}: {message}"
        client_socket.send(full_message.encode())

# Закрываем соединение
client_socket.close()
print("Выход из чата")
