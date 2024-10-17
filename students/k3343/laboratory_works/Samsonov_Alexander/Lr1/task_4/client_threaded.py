from socket import socket, AF_INET, SOCK_STREAM
import threading

is_active = True


def receive_messages(client_socket: socket) -> None:
    """
    Сервис для приема сообщений, работает в отдельном потоке от
    отправки сообщений
    :param client_socket: Сокет пользователя, в который принимается сообщения
    :type client_socket: socket
    :return: None
    :rtype: None
    """
    global is_active

    while is_active:  # I tried to gracefully close threads, it didn't work
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except ConnectionResetError or KeyboardInterrupt:
            is_active = False


def send_messages(client_socket: socket) -> None:
    """
    Сервис для отправки сообщения на сервер. Работает параллельно с приемом,
    в отдельном потоке.
    :param client_socket: Сокет пользователя, от которого высылается сообщение
    :type client_socket: socket
    :return: None
    :rtype: None
    """
    global is_active

    while is_active:  # I tried to gracefully close threads, it didn't work
        try:
            message = input()  # gather a message and send it
            if message in ('', 'quit', 'exit'):
                is_active = False
                break
            client_socket.send(message.encode('utf-8'))
        except ConnectionResetError or KeyboardInterrupt:
            is_active = False


def start_client(socket_address: tuple[str, int] = ('localhost', 12345)) -> None:
    """
    Создает клиента для многопользовательского чата на заданном сокете
    :param socket_address:  Tuple с указанием ip адреса и порта для сокета.
    ('localhost', 12345) по умолчанию
    :type socket_address: tuple[str, int]
    :return: None
    :rtype: None
    """
    name = input('Enter your name: ')
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(socket_address)  # server assumes, that your first message will be your name
    client_socket.send(name.encode('utf-8'))

    # Launching 2 threads to communicate back and forth
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
