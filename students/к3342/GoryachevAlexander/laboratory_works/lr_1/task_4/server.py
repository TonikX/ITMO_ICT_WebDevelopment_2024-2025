import socket
import threading

clients = []


def handle_client(client_socket, client_address):
    print(f"Новое подключение: {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Сообщение от {client_address}: {message}")

            broadcast(message, client_socket)
    except ConnectionResetError:
        print(f"Клиент {client_address} отключился.")
    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)
    print("Сервер запущен. Ожидание подключений...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()