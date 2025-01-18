# Задание 1: UDP-сервер и клиент
## Описание

Клиент отправляет серверу сообщение "Hello, server", сервер отображает его и отвечает клиенту "Hello, client".

### Серверная часть
```
import socket

# Создаем UDP-сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 12345))

print("Сервер запущен и ожидает сообщений...")

while True:
    # Получаем сообщение от клиента
    data, addr = sock.recvfrom(1024)
    print(f"Получено сообщение от {addr}: {data.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    sock.sendto(response.encode(), addr)

```
### Клиентская часть
```
import socket

# Создаем UDP-сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
sock.sendto(message.encode(), ('localhost', 12345))

# Получаем ответ от сервера
data, server = sock.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

sock.close()
```