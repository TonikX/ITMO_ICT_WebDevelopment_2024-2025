import socket
import threading

# Настройки клиента
HOST = 'localhost'
PORT = 8080

# Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Ошибка при получении сообщения.")
            client_socket.close()
            break

# Настройка клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, args=(client_socket,)).start()

# Ввод имени пользователя
username = input("Введите ваше имя: ")
client_socket.send(username.encode())

# Основной цикл для отправки сообщений
while True:
    message = input()
    if message.lower() == 'выход':
        break
    client_socket.send(message.encode())

client_socket.close()
