import socket
import threading

# Список для хранения подключений клиентов
clients = []


# Функция для обработки сообщений от клиента
def handle_client(client_socket, client_address):
    print(f"Новое подключение: {client_address}")
    clients.append(client_socket)

    try:
        while True:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"Сообщение от {client_address}: {message}")
            broadcast_message(message, client_socket)

    except ConnectionResetError:
        print(f"Клиент {client_address} отключился.")
    finally:
        # Удаляем клиента из списка и закрываем сокет
        clients.remove(client_socket)
        client_socket.close()


# Функция для отправки сообщения всем клиентам
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Не отправляем сообщение отправителю
            try:
                client.send(message.encode('utf-8'))
            except:
                # Удаляем клиента, если отправка не удалась
                client.close()
                clients.remove(client)


# Функция запуска сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Сервер запущен и ожидает подключения клиентов...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
