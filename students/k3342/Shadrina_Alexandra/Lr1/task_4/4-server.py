import socket
import threading

clients = {}


def broadcast(message, sender_socket=None):
    for client in list(clients):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]


def handle_client(client_socket):
    try:
        client_name = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = client_name
        print(f"{client_name} подключился.")

        broadcast(f"{client_name} присоединился к чату.", client_socket)

        while True:
            message = client_socket.recv(1024)
            if message:
                message = message.decode('utf-8')
                print(f"{client_name}: {message}")
                broadcast(f"{client_name}: {message}", client_socket)
            else:
                break
    except:
        pass
    finally:
        if client_socket in clients:
            print(f"{clients[client_socket]} отключился.")
            broadcast(f"{clients[client_socket]} покинул(-а) чат.", client_socket)
            del clients[client_socket]
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)

    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
