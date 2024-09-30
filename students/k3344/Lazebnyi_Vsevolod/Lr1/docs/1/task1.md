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

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind(('localhost', 8080))

    print("Сервер запущен на порту 8080...")

    while True:
        client_message, client_address = server_socket.recvfrom(1024)
        print("Recieved message:", client_message.decode())
        server_socket.sendto("Hello, client".encode(), client_address)
        socket.socket.close()
```
#### client.py
``` 
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('localhost', 8080)
try:
    client_socket.sendto("Hello, server!".encode(), client_address)
    server_message, server_address = client_socket.recvfrom(1024)
    print(f"Получено сообщение от сервера: {server_message.decode()}")
finally:
    client_socket.close()
```

### Пояснение:
В рамках данного задания был реализован простой UDP-сервер, при запуске которого после сообщения клиента, он же получает в ответ сообщение от сервера. При реализации используется дейтаграммный сокет SOCK_DGRAM, в основе которого лежит протокол UDP. Такие сокеты не требуют установления явного соединения между ними. Сообщение отправляется указанному сокету и, соответственно, может получаться от указанного сокета. 