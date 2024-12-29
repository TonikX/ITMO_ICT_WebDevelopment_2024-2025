# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client». Реализовать с помощью протокола UDP.

## Реализация
В данном задании создается клиент-серверное приложение для обмена сообщениями с использованием протокола UDP. Так, клиент отправляет сообщение «Hello, server» на сервер, который принимает это сообщение и выводит его на экран, после чего отправляет обратно ответ «Hello, client». Клиент получает ответ (он отображается в консоли), и соединение завершается.
### Сервер
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))
print("Сервер запущен на порту 8080...")

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'Получено сообщение от {client_address}: {message.decode()}')

    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
```
### Клиент
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8080)

client_socket.sendto(b'Hello, server', server_address)

response, server = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```