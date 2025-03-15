# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

## Код
Серверная часть
```python
import socket

# Создание UDP-сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязка сокета к IP и порту
server_address = ('127.0.0.1', 65432)
server_socket.bind(server_address)

print("UDP сервер запущен и ожидает сообщений...")

while True:
    # Ожидание сообщения от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Получено сообщение от {client_address}: {data.decode()}")

    # Ответ клиенту (опционально)
    response = "Hello client"
    server_socket.sendto(response.encode(), client_address)
```

Клиентская часть
```python
import socket

# Создание UDP-сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('127.0.0.1', 65432)

# Отправка сообщения серверу
message = "hello server"
client_socket.sendto(message.encode(), server_address)

# Получение ответа от сервера (опционально)
data, server = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрытие сокета
client_socket.close()
```
