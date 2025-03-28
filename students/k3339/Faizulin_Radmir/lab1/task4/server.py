import socket
import threading

HOST = '127.0.0.1'  # Локальный хост
PORT = 12345  # Порт для прослушивания

clients = []


def broadcast(message, sender_socket=None):
    # Рассылка сообщения всем клиентам, кроме отправителя.
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
                clients.remove(client)


def handle_client(client_socket, client_address):
    # Обработка сообщений от клиента.
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            message = f"{client_address}: {message}"
            broadcast(message, sender_socket=client_socket)
        except Exception as e:
            print(f"Ошибка связи с клиентом: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()


def start_server():
    # Запуск сервера.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Новое подключение: {client_address}")

        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
