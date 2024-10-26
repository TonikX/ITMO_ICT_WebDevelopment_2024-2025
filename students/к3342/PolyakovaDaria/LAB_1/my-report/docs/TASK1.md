# Задание №1

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

## UDP Сервер

Этот код реализует UDP-клиент на Python, который отправляет сообщение "Hello, server" на локальный сервер, работающий на порту 8080. Сначала создается сокет для UDP-соединения. Затем клиент отправляет закодированное сообщение на указанный адрес и порт. После этого он ожидает и получает ответ от сервера, который затем декодируется и выводится на экран. В конце работы сокет закрывается.

```python
import socket

HOST = 'localhost'
PORT = 8080

# Создаем сокет для UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}...")

while True:
    # Получаем сообщение от клиента
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента: {message.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```

## UDP Клиент

Этот код реализует UDP-клиент на Python, который отправляет сообщение на сервер и получает ответ. Устанавливаются адрес сервера (`localhost`) и порт (`8080`). Затем создается UDP-сокет с помощью `socket.socket()`. Клиент отправляет сообщение "Hello, server" на сервер и ожидает ответ. Полученный ответ выводится на экран, после чего сокет закрывается для освобождения ресурсов. Код демонстрирует основную работу с UDP-сетевыми сокетами в Python.

```python
import socket

# Параметры сервера
HOST = 'localhost'  # Адрес сервера
PORT = 8080         # Порт сервера

# Создаем сокет для UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для отправки серверу
message = "Hello, server"
client_socket.sendto(message.encode(), (HOST, PORT))

# Получаем ответ от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")

# Закрываем сокет
client_socket.close()
```

