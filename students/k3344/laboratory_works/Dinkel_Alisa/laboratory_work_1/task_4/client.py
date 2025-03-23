import socket
import threading


HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8082         # Порт, на котором будет работать сервер

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect((HOST, PORT))


# Функция для приема сообщений
def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            print(msg)
        except:
            client_socket.close()
            break


# Запускаем поток для приема сообщений
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Ввод имени
name = input("Введите ваше имя: ")
client_socket.send(name.encode("utf-8"))

# Основной ввод сообщений
while True:
    msg = input()
    if msg.lower() == "exit":
        client_socket.send(msg.encode("utf-8"))
        break
    client_socket.send(msg.encode("utf-8"))

# Закрываем соединение
client_socket.close()