import socket
import threading

# Настройки сервера
HOST = 'localhost'
PORT = 8080

# Список клиентов
clients = []
usernames = []

# Функция для обработки сообщений от клиентов
def handle_client(client_socket, address):
    print(f"{address} подключился.")
    #client_socket.send("Введите ваше имя:".encode())
    username = client_socket.recv(1024).decode()
    usernames.append(username)
    clients.append(client_socket)

    broadcast(f"{username} присоединился к чату.".encode(), client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{username}: {message.decode()}".encode(), client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

# Функция для рассылки сообщений всем клиентам
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

# Функция для удаления клиента из списков
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        username = usernames[index]
        usernames.remove(username)
        broadcast(f"{username} покинул чат.".encode(), client_socket)

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Сервер запущен...")

# Запуск обработки клиентов
while True:
    client_socket, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, address)).start()
