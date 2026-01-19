from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Создаем сокет
server_socket = socket(AF_INET, SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения
server_socket.listen(5)
print("Чат-сервер запущен на localhost:8080")
print("Ожидание подключений...")

# Список для хранения подключенных клиентов
clients = []
nicknames = []


def broadcast(message: bytes, sender_client: socket = None) -> None:
    """Отправка сообщения всем клиентам, кроме отправителя"""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                # Если отправка не удалась, удаляем клиента
                clients.remove(client)


def handle_client(client: socket) -> None:
    """Обработка сообщений от клиента"""
    while True:
        try:
            # Получаем сообщение от клиента
            message = client.recv(1024)
            if message:
                print(message.decode())
                # Отправляем сообщение всем клиентам
                broadcast(message, client)
            else:
                # Пустое сообщение означает отключение клиента
                remove_client(client)
                break
        except:
            remove_client(client)
            break


def remove_client(client: socket) -> None:
    """Удаление клиента из списка"""
    if client in clients:
        leave_nickname = nicknames[clients.index(client)]

        # Удаляем клиента из списков
        clients.remove(client)
        nicknames.remove(leave_nickname)

        # Сообщаем о выходе пользователя
        leave_message = f"{leave_nickname} покинул чат".encode()
        print(leave_message.decode())
        broadcast(leave_message)

        # Закрываем соединение
        client.close()


while True:
    # Принимаем соединение от клиента
    client_socket, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Запрашиваем никнейм
    client_socket.send("Введите ваш никнейм: ".encode())
    nickname = client_socket.recv(4096).decode()

    # Проверяем, занят ли никнейм
    if nickname in nicknames:
        error_message = "Этот никнейм уже занят. Подключение закрыто.".encode()
        client_socket.send(error_message)
        client_socket.close()
        print(f"Отклонено подключение от {client_address}: никнейм '{nickname}' уже занят")
        continue

    # Добавляем клиента в списки
    nicknames.append(nickname)
    clients.append(client_socket)

    # Сообщаем о новом пользователе
    join_message = f"{nickname} присоединился к чату!".encode()
    print(join_message.decode())
    broadcast(join_message)

    # Запускаем поток для обработки клиента
    client_thread = Thread(target=handle_client, args=(client_socket,))
    client_thread.daemon = True
    client_thread.start()
