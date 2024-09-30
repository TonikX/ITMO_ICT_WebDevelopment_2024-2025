import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002


def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break


def start_client():
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())

    client_socket.close()


if __name__ == "__main__":
    start_client()