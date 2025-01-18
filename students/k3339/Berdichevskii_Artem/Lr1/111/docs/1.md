# Задание 1

### Описание задачи

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно 
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно 
отобразиться у клиента.

### Реализация

##### Стэк
* Python: 3.10
* Библиотека: socket

**Серверная часть:**
```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 65432))

while True :
    data, address = sock.recvfrom(1024)
    print(f'Получено сообщение от {address}: {data.decode()}')

    response = 'Hello, client'
    sock.sendto(response.encode(), address)
```

**Клиентская часть:**
```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'Hello, server'
sock.sendto(message.encode(), ('127.0.0.1', 65432))

data, address = sock.recvfrom(1024)
print(f'Получено сообщение от {address}: {data.decode()}')
```