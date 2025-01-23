# Задание 4

## Текст задания

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

## Требования

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.

## Запуск

1. Запуск сервера

```python
python3 server.py
```

2. Запуск клиентов

```python
python3 client.py
```

## Код

### client.py

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
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

while True:
    message = input()
    if message:
        client_socket.send(message.encode('utf-8'))
```

### server.py

```python
import socket
import threading

clients = []

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

def handle_client(client_connection, client_address):
    client_port = client_address[1]
    print(f"Новое подключение: {client_port}")
    while True:
        try:
            message = client_connection.recv(1024).decode()
            if message:
                print(f"Сообщение от {client_port}: {message}")
                broadcast_message(f"{client_port}: {message}", client_connection)
            else:
                remove_client(client_connection)
                break
        except:
            remove_client(client_connection)
            break

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_connection):
    if client_connection in clients:
        clients.remove(client_connection)
        client_connection.close()

while True:
    client_connection, client_address = server_socket.accept()
    clients.append(client_connection)

    thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
    thread.start()
```

## Описание работы кода

### Клиентская часть

- Создается TCP-сокет, подключающийся к серверу по адресу localhost и порту 8080
- Функция receive_messages запущена в отдельном потоке, непрерывно принимая сообщения от сервера и выводя их в консоль
- Основной поток ожидает ввода сообщений пользователем и отправляет их на сервер

### Серверная часть 

- Создается TCP-сервер, принимающий входящие подключения от клиентов на порту 8080
- С помощью функции handle_client сервер обрабатывает сообщения от каждого клиента в отдельном потоке, передавая их через функцию broadcast_message всем активным клиентам, кроме отправителя
- Функция remove_client отключает клиента и удаляет его из списка при завершении соединения или ошибке

### Многопользовательская поддержка

- Библиотека threading позволяет запускать обработку каждого клиента в отдельном потоке, обеспечивая одновременное взаимодействие нескольких пользователей, сообщения рассылаются всем участникам чата