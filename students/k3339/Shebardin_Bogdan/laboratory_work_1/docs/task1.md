# Задание 1. Обмен сообщениями по UDP

## Постановка

Реализовать клиент-серверное приложение: клиент отправляет сообщение «Hello, server», сервер его отображает и отвечает «Hello, client».

**Требования:**
- Библиотека `socket`
- Протокол UDP

## Архитектура

UDP — протокол без установления соединения. Обмен идёт через `sendto()` и `recvfrom()`. Предварительное `connect()` не требуется.

## Код сервера `server_for_task1.py`

```python
import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('localhost', 8080))

while True:
    data, addr = server_sock.recvfrom(1024)
    print(
        f'Получено сообщение "{data.decode("utf-8")}" от адреса'
        f' {addr}'
    )
    reply = b'Hello, Client!'
    server_sock.sendto(reply, addr)
```

## Код клиента `client_for_task1.py`

```python
import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = b'Hello, Server!'
client_sock.sendto(message, ('localhost', 8080))

data, addr = client_sock.recvfrom(1024)
print(f'ответ от сервера: {data.decode("utf-8")}')

client_sock.close()
```

##  Результат

Терминал 1 (сервер)
```text
Получено сообщение "Hello, Server!" от адреса ('127.0.0.1', 61390)
```
Терминал 2 (клиент)
```text
ответ от сервера: Hello, Client!
```