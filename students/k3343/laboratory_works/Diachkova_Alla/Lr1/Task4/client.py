import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
buffersize = 1024


def receive_message(target_socket):
    while True:
        try:
            message = target_socket.recv(buffersize)
            if not message:
                break
            print(message.decode())
        except:
            break


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    threading.Thread(target=receive_message, args=(client_socket,)).start()
    while True:
        message = input()
        if message == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode())


if __name__ == "__main__":
    connect()
