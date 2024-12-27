# Задание 4

Реализовать многопользовательский чат. 

**Требования:**

Обязательно использовать библиотеку socket.
Для многопользовательского чата необходимо использовать библиотеку threading и протокол TCP.

Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

## Реализация
На основе TCP реализуется многопользовательский чат с использованием библиотек socket и threading. Сервер принимает подключения от клиентов, регистрирует их в словаре и обеспечивает обмен сообщениями между ними, отправляя сообщения всем подключенным пользователям (кроме отправителя). Каждый клиент запускает отдельный поток для обработки входящих сообщений и отправки сообщений в чат. Так, клиенты могут присоединяться к чату, отправлять и получать сообщения.
### Сервер
```python
import socket
import threading

clients = {}


def broadcast(message, sender_socket=None):
    for client in list(clients):
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]


def handle_client(client_socket):
    try:
        client_name = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = client_name
        print(f"{client_name} подключился.")

        broadcast(f"{client_name} присоединился к чату.", client_socket)

        while True:
            message = client_socket.recv(1024)
            if message:
                message = message.decode('utf-8')
                print(f"{client_name}: {message}")
                broadcast(f"{client_name}: {message}", client_socket)
            else:
                break
    except:
        pass
    finally:
        if client_socket in clients:
            print(f"{clients[client_socket]} отключился.")
            broadcast(f"{clients[client_socket]} покинул(-а) чат.", client_socket)
            del clients[client_socket]
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)

    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
```
### Клиент
```python
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Соединение с сервером потеряно")
                client_socket.close()
                break
        except:
            print("Ошибка при получении сообщения")
            client_socket.close()
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    username = input("Введите ваше имя: ")
    client_socket.send(username.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":
    start_client()

```