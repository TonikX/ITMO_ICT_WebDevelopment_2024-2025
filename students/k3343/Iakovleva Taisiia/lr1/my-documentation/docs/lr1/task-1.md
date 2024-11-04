# Задание 1

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Требования

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

## Запуск

1. Запуск сервера

```python
python3 server.py
```

2. Запуск клиента

```python
python3 client.py
```

## Код

### client.py

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

client_socket.sendall(f'Hello, server'.encode('utf-8'))

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```

### server.py

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:

    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    response = 'Hello, client'
    client_connection.sendall(response.encode())

    client_connection.close()
```