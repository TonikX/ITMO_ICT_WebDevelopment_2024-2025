from socket import socket, AF_INET, SOCK_STREAM
import threading

active = True


def receive_messages(client_socket: socket) -> None:
    global active
    while active:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except (ConnectionResetError, KeyboardInterrupt):
            active = False


def send_messages(client_socket: socket) -> None:
    global active
    while active:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
        except (ConnectionResetError, KeyboardInterrupt):
            active = False


def start(socket_address: tuple[str, int] = ('localhost', 2024)) -> None:
    name = input('Name: ')

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(socket_address)
    client_socket.send(name.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    receive_thread.join()
    send_thread.join()


if __name__ == "__main__":
    try:
        start()
    except:
        pass