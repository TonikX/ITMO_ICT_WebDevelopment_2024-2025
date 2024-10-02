import socket
import threading

# Настройки сервера
HOST = 'localhost'  # Локальный хост
PORT = 12345        # Порт для прослушивания

# Список клиентов
clients = []
usernames = {}

def broadcast(message, _client_socket):
    """Функция для отправки сообщения всем подключенным пользователям."""
    for client in clients:
        if client != _client_socket:  # Не отправляем сообщение отправителю
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(client_socket):
    """Функция для обработки клиента."""
    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024)
            if message:
                username = usernames[client_socket]
                formatted_message = f"{username}: {message.decode('utf-8')}".encode('utf-8')
                print(f"[DEBUG] {formatted_message.decode('utf-8')}")
                broadcast(formatted_message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

def remove_client(client_socket):
    """Удаляем клиента из списка клиентов."""
    if client_socket in clients:
        clients.remove(client_socket)
        print(f"[INFO] Клиент {usernames[client_socket]} отключился.")
        broadcast(f"{usernames[client_socket]} покинул чат.\n".encode('utf-8'), client_socket)
        del usernames[client_socket]
        client_socket.close()

def receive_connections():
    """Функция для принятия новых подключений."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("[INFO] Сервер запущен и ожидает подключений...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[INFO] Новое подключение: {client_address}")

        # Получаем имя пользователя
        client_socket.send("Введите ваше имя пользователя: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        clients.append(client_socket)

        print(f"[INFO] Имя пользователя {username} присоединилось.")
        broadcast(f"{username} присоединился к чату.\n".encode('utf-8'), client_socket)

        # Запуск нового потока для обработки клиента
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

receive_connections()


