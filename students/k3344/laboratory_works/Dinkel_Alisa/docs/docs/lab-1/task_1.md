# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

- Язык реализации: Python
- Протокол: UDP
- Используемые библиотеки: socket

## Реализация
client.py
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Отправляем сообщение серверу
client_socket.sendall(b'Hello, server')

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()
```
server.py
```python
import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем сообщение от клиента
    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    # Отправляем ответ клиенту
    response = 'Hello, client'
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()
```
## Запуск
- Запустите сервер:
```bash
python server.py
```
- Запустите клиента:
```bash
python client.py
```