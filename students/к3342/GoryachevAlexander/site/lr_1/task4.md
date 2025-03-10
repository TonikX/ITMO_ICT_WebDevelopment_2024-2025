# Задание 4

## Суть задания
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

Обязательно использовать библиотеку socket.
Для многопользовательского чата необходимо использовать библиотеку threading.
Реализация:

Протокол TCP: 100% баллов.
Протокол UDP: 80% баллов.
Для UDP используйте threading для получения сообщений на клиенте.
Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Сервер
Сервер принимает сообщения от нескольких клиентов и передает всем клиентам каждое сообщение. Для каждого клиента выделяется отдельный поток
```python
import socket
import threading

clients = []


def handle_client(client_socket, client_address):
    print(f"Новое подключение: {client_address}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Сообщение от {client_address}: {message}")

            broadcast(message, client_socket)
    except ConnectionResetError:
        print(f"Клиент {client_address} отключился.")
    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)
    print("Сервер запущен. Ожидание подключений...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
```
### Клиент
Клиент подключается к серверу и постоянно пытается получить от него сообщение. Также в клиенте реализована возможность отослать сообщение серверу
```python
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Соединение с сервером потеряно.")
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))  # Подключение к серверу
    print("Подключено к чату. Введите сообщения ниже:")

    # Запускаем поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            client_socket.send(message.encode())
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
```