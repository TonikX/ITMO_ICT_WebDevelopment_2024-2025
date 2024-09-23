import socket
import threading

HOST = 'localhost'
PORT = 9000
BUFF_SIZE = 1024


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFF_SIZE).decode()
            if message:
                print(message)
            else:
                break
        except ConnectionResetError:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    username = input("Enter your username: ")
    client_socket.send(username.encode())

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message:
            client_socket.send(message.encode())


if __name__ == "__main__":
    start_client()
