# Лабораторная 1, Задание 4
## Условие
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.
### Требования:
- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
### Реализация:
Реализация:
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте threading для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

## Решение

Выбран вариант с многопользовательским чатом с TCP.

`server.py`
```
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

```
`client.py`
```
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

```
