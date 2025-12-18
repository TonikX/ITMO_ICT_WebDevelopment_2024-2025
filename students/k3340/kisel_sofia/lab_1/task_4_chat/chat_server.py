import socket
import threading
from typing import Dict


clients: Dict[socket.socket, str] = {}
clients_lock = threading.Lock()


def broadcast(message: str) -> None:
    with clients_lock:
        for client in list(clients):
            try:
                client.send(message.encode('utf-8'))
            except Exception:
                client.close()
                del clients[client]


def handle_client(client_socket: socket.socket, addr):
    nickname = client_socket.recv(1024).decode()

    with clients_lock:
        clients[client_socket] = nickname

    broadcast(f'{nickname} подключился к чату')

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            broadcast(f'{nickname}: {data.decode()}')
        except Exception:
            break

    with clients_lock:
        del clients[client_socket]

    broadcast(f'{nickname} покинул чат')
    client_socket.close()


def run_server(server_host: str = '127.0.0.1', server_port: int = 8082):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen()

        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr),
                daemon=True
            )
            thread.start()


if __name__ == '__main__':
    run_server()
