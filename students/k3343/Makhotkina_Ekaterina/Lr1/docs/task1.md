Задание 1: 
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

Листинг кода серверной части:

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(f'{message.decode()}')
    response = 'Hello client!'
    server_socket.sendto(response.encode(), client_address)
```

Листинг кода клиентской части:

```python
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)
message = 'Hello, server!'
client_socket.sendto(message.encode(), server_address)
response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
```

Объяснение:

Запускаем файл севера, потом клиента; происходит обмен сообщениями. Обмен происходит при помощи протокола UDP(параметр socket.SOCK_DGRAM)