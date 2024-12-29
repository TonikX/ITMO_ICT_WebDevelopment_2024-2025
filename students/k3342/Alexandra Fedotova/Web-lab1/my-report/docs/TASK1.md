# **Задание 1**

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## **Tребования**:
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола UDP.

## **Серверная часть**:

```python
import socket

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к IP и порту
server_socket.bind(('localhost', 8080))

print("Сервер запущен на порту 8080...")

while True:
    # Принимаем сообщение от клиента
    message, client_address = server_socket.recvfrom(1024)
    print(f"Сообщение от {client_address}: {message.decode()}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```
## **Реализация клиентской части**:

```python
import socket

# Создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для отправки серверу
server_message = "Hello, server"

# Отправляем сообщение серверу
client_socket.sendto(server_message.encode(), ('localhost', 8080))

# Получаем ответ от сервера
response, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {response.decode()}")

# Закрываем сокет
client_socket.close()
```