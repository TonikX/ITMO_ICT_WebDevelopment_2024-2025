# Задание 1:

## Описание задания
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Требования
- Обязательно использовать библиотеку `socket`.
- Реализовать взаимодействие с помощью протокола UDP.

## Реализация

### Клиентская часть
Клиент отправляет сообщение на сервер, используя протокол UDP. После отправки сообщения клиент ожидает ответ от сервера.

```python
import socket

IP = 'localhost'
PORT = 8080
message = 'Hello, server'

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.sendto(message.encode(), (IP, PORT))

response, server_address = client_sock.recvfrom(1024)
print(response.decode())
client_sock.close()
```
### Серверная часть
Сервер принимает сообщение от клиента, отображает его и отправляет обратно ответное сообщение.

```python
import socket

IP = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((IP, PORT))

response, client_address = server_sock.recvfrom(1024)
print(response.decode())

message = 'Hello, client'
server_sock.sendto(message.encode(), client_address)
server_sock.close()
```