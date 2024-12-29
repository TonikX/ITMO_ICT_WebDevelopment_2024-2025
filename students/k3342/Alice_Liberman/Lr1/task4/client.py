from socket import socket, AF_INET, SOCK_STREAM
import threading

is_active = True


def receive_messages(client_socket: socket) -> None:

    global is_active

    while is_active:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except ConnectionResetError or KeyboardInterrupt:
            is_active = False


def send_messages(client_socket: socket) -> None:

    global is_active

    while is_active:
        try:
            message = input()
            if message in ('', 'quit', 'exit'):
                is_active = False
                break
            client_socket.send(message.encode('utf-8'))
        except ConnectionResetError or KeyboardInterrupt:
            is_active = False


def start_client(socket_address: tuple[str, int] = ('localhost', 12345)) -> None:

    name = input('Введите имя: ')
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
        start_client()
    except:
        pass