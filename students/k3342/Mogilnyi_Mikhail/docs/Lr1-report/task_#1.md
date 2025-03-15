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

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b'HELLO FROM CLIENT', (HOST, PORT))

data, addr = client.recvfrom(BUFFER_SIZE)
print(data.decode())
```

### Сервер
Сервер слушает входящие сообщения и отвечает на них. Код сервера представлен ниже:

```python
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1313
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

while True:
    data, addr = server.recvfrom(BUFFER_SIZE)
    print(data.decode())
    
    server.sendto(b'HELLO FROM SERVER', addr)
```