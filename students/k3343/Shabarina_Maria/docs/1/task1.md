## Задание №1. UDP-сервер

### Описание: 
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования:
* Обязательно использовать библиотеку socket
* Реализовать с помощью протокола UDP.

### Листинг кода:
#### server.py
```
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 1234))

print("Server started")

client_message, client_address = server_socket.recvfrom(1024)
print("Recieved message:", client_message.decode())
server_socket.sendto("Hello, client".encode(), client_address)
```
#### client.py
``` 
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("Hello, server".encode(), ("localhost", 1234))

server_message, server_address = client_socket.recvfrom(1024)
print("Recieved message:", server_message.decode())
```

### Пояснение:
В рамках данного задания был реализован простой UDP-сервер, при запуске которого после сообщения клиента, он же получает в ответ сообщение от сервера. При реализации используется дейтаграммный сокет SOCK_DGRAM, в основе которого лежит протокол UDP. Такие сокеты не требуют установления явного соединения между ними. Сообщение отправляется указанному сокету и, соответственно, может получаться от указанного сокета. 