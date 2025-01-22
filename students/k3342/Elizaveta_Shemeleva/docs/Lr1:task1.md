# Отчет по Заданию 1: UDP Чат

## Описание задания
В этом задании необходимо было реализовать клиент и сервер с использованием протокола UDP. Клиент отправляет сообщение серверу, а сервер отвечает клиенту.

## Реализация

### Сервер:
```
import socket

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

print("Сервер ожидает сообщение...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от клиента: {message.decode()}")

    # Ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```
### Клиент:
```
import socket

# Настройка клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)

# Отправка сообщения серверу
message = "Hello, server"
client_socket.sendto(message.encode(), server_address)

# Получение ответа
response, _ = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")
```
## Вывод:
Взаимодействие по протоколу UDP было успешно реализовано.
