# Задание 1

## Суть задания

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

**Требования**:
Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

### Клиент

Клиент отправляет сообщение серверу и ожидает ответ. Код клиента представлен ниже:

```python
import socket

# Настройка клиента
SERVER_IP = '127.0.0.1'  # IP-адрес сервера
SERVER_PORT = 12345       # Порт сервера
CLIENT_PORT = 54321       

# Создание сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1', CLIENT_PORT))

# Отправка сообщения серверу
message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Получение ответа от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")
```

### Сервер
Сервер слушает входящие сообщения и отвечает на них. Код сервера представлен ниже:

```python
import socket

SERVER_IP = '127.0.0.1'  # Локальный IP-адрес
SERVER_PORT = 12345       # Порт для прослушивания

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"UDP сервер запущен на {SERVER_IP}:{SERVER_PORT}")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента {client_address}: {data.decode()}")

    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```