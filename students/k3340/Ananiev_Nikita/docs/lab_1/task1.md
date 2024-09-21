## Задание 1: Реализовать клиент-серверное взаимодейстие с помощью сокетов и UDP протокола

Описание: <br> Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу
сообщение «Hello, server». Сообщение должно отразиться на стороне сервера.
Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно
отобразиться у клиента.

Код сервера:
```python
import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_socket.bind(('', 8080))

max_user_conn, listening = 1, True
serv_response = b"Hello, client"

while listening:
    client_data, addr = serv_socket.recvfrom(1024)
    if not client_data:
        break
    print(client_data)
    serv_socket.sendto(serv_response, addr)

serv_socket.close()
```
Код клиента:
```python
import sys
import socket

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()


getting_data = True
while getting_data:
    message = bytes(input(), 'utf-8')
    client_socket.sendto(message, ('localhost', 8080))
    serv_response = client_socket.recv(1024)
    if not serv_response:
        client_socket.close()
        break
    print(serv_response)
```