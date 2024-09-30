import socket
import threading


SERVER_ADDRESS = ("192.168.0.102", 1234)
BUFFER_SIZE = 1024
clients: list[socket.socket] = []


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()
    print(f"Listening on {SERVER_ADDRESS}")

    while True:
        accept_client(server_socket)


def accept_client(server_socket: socket.socket):
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    send_all_clients(f"{client_address} has joined the chat.")

    thread = threading.Thread(
        target=serve_client,
        args=(server_socket, client_socket, client_address),
    )
    thread.start()


def serve_client(
    server_sock: socket.socket,
    client_sock: socket.socket,
    client_addr,
):
    while True:
        message = client_sock.recv(BUFFER_SIZE).decode()
        response = f"{client_addr}: {message}"
        send_all_clients_except_me(client_sock, response)


def send_all_clients(message: str):
    for client in clients:
        client.sendall(message.encode())


def send_all_clients_except_me(sender: socket.socket, message: str):
    for client in clients:
        if client == sender:
            continue
        client.sendall(message.encode())


if __name__ == "__main__":
    run_server()
