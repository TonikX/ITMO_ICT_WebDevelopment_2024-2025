import socket
import threading


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)


def start_client(host='localhost', port=8083):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":
    start_client()
