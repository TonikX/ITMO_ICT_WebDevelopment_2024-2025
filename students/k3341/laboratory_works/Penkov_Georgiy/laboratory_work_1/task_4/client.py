import socket
import threading

SERVER_ADDRESS = ("localhost", 1234)
BUFFER_SIZE = 1024


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)

    recv_thread = threading.Thread(
        target=recv_from_server, args=(client_socket,), daemon=True
    )
    recv_thread.start()

    send_to_server(client_socket)


def recv_from_server(client_socket: socket.socket):
    while True:
        message = client_socket.recv(BUFFER_SIZE).decode()
        print(message)


def send_to_server(client_socket: socket.socket):
    while True:
        message = input()
        client_socket.sendall(message.encode())
        if message.lower() == "exit":
            break


if __name__ == "__main__":
    run_client()
