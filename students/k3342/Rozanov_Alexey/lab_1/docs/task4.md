# Задание 4

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте 
многопользовательский чат.

Был реализован многопользовательский чат в рамках примера работы приведен пример с 3 пользователями

## Файл server.py

Код:

```python
import socket
import threading


def broadcast_message(message, current_client):
    """
    Sending messages to all clients
    :param message: text of message
    :param current_client: current client info
    """
    for client in connected_clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)


def handle_client_connection(client_socket):
    """
    client connections handler
    :param client_socket:
    """
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Получено сообщение от клиента: {message.decode('utf-8')}")
                broadcast_message(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue


def remove_client(client_socket):
    if client_socket in connected_clients:
        connected_clients.remove(client_socket)


def start_server(host='127.0.0.1', port=8088):
    """
    server starter and worker
    :param host:
    :param port:
    :return:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        print(f"Сервер запущен на порту {port}")
        server_socket.listen()
        print("Ожидание подключений...")
    except Exception as error:
        print(f"Ошибка запуска сервера: {error}")
        return

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Подключён клиент с адреса: {client_address}")
            connected_clients.append(client_socket)
            threading.Thread(target=handle_client_connection, args=(client_socket,)).start()
        except Exception as error:
            print(f"Ошибка при подключении клиента: {error}")


if __name__ == "__main__":
    connected_clients = []
    start_server()
```

Скриншот работы в режиме подключения 3 пользователей:

[Скриншот работы с 3 подключениями](imgs/task4_server.png)

## Файл user.py (все файлы одинаковые)

Код:

```python
import socket
import threading


def receive_server_messages(client_socket):
    """
    reciever for messages
    :param client_socket:
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\nПолучено сообщение: {message} \nВведите сообщение:")
            else:
                break
        except Exception as error:
            print(f"Ошибка при получении сообщения: {error}")
            client_socket.close()
            break


def send_client_messages(client_socket):
    """
    sender of messages
    :param client_socket:
    """
    while True:
        try:
            message = input("Введите сообщение: ")
            client_socket.send(message.encode('utf-8'))
        except Exception as error:
            print(f"Ошибка при отправке сообщения: {error}")
            client_socket.close()
            break


def start_client():
    """
    client starter
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 8088))
        print("Соединение с сервером установлено.")
    except Exception as error:
        print(f"Не удалось подключиться к серверу: {error}")
        return

    threading.Thread(target=receive_server_messages, args=(client_socket,)).start()
    threading.Thread(target=send_client_messages, args=(client_socket,)).start()


if __name__ == "__main__":
    start_client()
```

Скриншоты работы в режиме подключения 3 пользователей:

[Скриншот отправителя](imgs/task4_client_sender.png)

[Скриншот получателя](imgs/task4_client_reciever.png)