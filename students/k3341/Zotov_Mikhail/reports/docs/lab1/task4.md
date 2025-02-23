# Задание 4<br><br>

### Условие

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

#### Требования:
- Обязательно использовать библиотеку `socket`.
- Для многопользовательского чата необходимо использовать библиотеку `threading`.

#### Реализация:
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте `threading` для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

Я реализовал многопользовательский чат  помощью протокола TCP.

---
### Код

#### Сервер
```python
import socket
import threading

members = {}  # nickname: client_socket


def start_chat(sock):
    while True:
        client_socket, client_address = sock.accept()
        print("Got connection from", client_address)

        threading.Thread(target=handle_clients, args=(client_socket,)).start()


def sending_messages(message, nick):
    for nickname in members.keys():
        if nickname != nick:
            members[nickname].sendall(message.encode())


def handle_clients(client):
    client.send("Enter your nickname to join the chat".encode())
    nickname = client.recv(1024).decode()
    members[nickname] = client
    sending_messages(f"New user joined: {nickname}", nickname)

    while True:
        try:
            message = client.recv(1024).decode()
            sending_messages(message, nickname)
        except Exception as error:
            client.sendall(f"This error occurred: {error}".encode())


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 2024))
    sock.listen(5)
    print("Server listening on port 2024")

    start_chat(sock)


if __name__ == '__main__':
    run()
```
#### Клиент
```python
import socket
import threading


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2024)
    sock.connect(server_address)
    message = sock.recv(1024)
    print(message.decode())
    nickname = input('Nickname: ')
    sock.send(nickname.encode())

    threading.Thread(target=accept_messages, args=(sock,)).start()
    threading.Thread(target=send_messages, args=(sock,)).start()


def send_messages(sock):
    while True:
        message = input("")
        sock.sendall(message.encode())


def accept_messages(sock):
    while True:
        message = sock.recv(1024)
        print(message.decode())


if __name__ == '__main__':
    run()
```