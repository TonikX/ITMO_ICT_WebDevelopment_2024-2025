import socket
import threading

HOST = 'localhost'
PORT = 9000
BUFF_SIZE = 1024
CONNECTIONS = 5

clients = {}
clients_lock = threading.Lock()


def handle_client(client_socket):
    username = client_socket.recv(BUFF_SIZE).decode()
    clients[client_socket] = username
    print(f"User '{username}' connected")

    try:
        while True:
            message = client_socket.recv(BUFF_SIZE).decode()
            if message:
                log_message(username, message)
                broadcast(f"{username}: {message}", client_socket)
            else:
                break
    except ConnectionResetError:
        pass
    finally:
        remove_client(client_socket)


def log_message(username, message):
    print(f"{username} sent: {message}")


def broadcast(message, sender_socket):
    for client in list(clients):
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Error sending message to {client}: {e}")
                remove_client(client)


def remove_client(client_socket):
    if client_socket in clients:
        username = clients.pop(client_socket)
        print(f"User {username} disconnected")
        client_socket.close()
    else:
        print(f"User {clients.pop(client_socket)} doesn't exist")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(CONNECTIONS)
    print(f"Server online on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    start_server()
