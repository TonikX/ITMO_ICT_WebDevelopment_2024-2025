import socket
import threading


type Socket = socket.socket

SERVER_ADDRESS = ("localhost", 1234)
BUFFER_SIZE = 1024
clients: list[Socket] = []


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()
    print(f"Listening on {SERVER_ADDRESS}")

    while True:
        accept_client(server_socket)


def accept_client(server_socket: Socket):
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    send_all_clients(f"{client_address} has joined the chat.")

    thread = threading.Thread(
        target=serve_client,
        args=(client_socket, client_address),
    )
    thread.start()


def serve_client(
    client_sock: Socket,
    client_addr,
):
    while True:
        message = client_sock.recv(BUFFER_SIZE).decode()
        if message.lower() == "exit":
            clients.remove(client_sock)
            send_all_clients(f"{client_addr} exited the chat.")
            client_sock.close()
            break
        response = f"{client_addr}: {message}"
        send_all_clients(response)


def send_all_clients(message: str):
    for client in clients:
        client.sendall(message.encode())


if __name__ == "__main__":
    run_server()
