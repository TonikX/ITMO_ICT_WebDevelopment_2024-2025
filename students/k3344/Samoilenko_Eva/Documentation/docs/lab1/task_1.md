### Задание 1:

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:

- Обязательно использовать библиотеку socket.

- Реализовать с помощью протокола UDP.


### Ход работы:

#### server.py

```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_address = ('localhost', 8080)
sock.bind(serv_address)

print('connected:', serv_address)

while True:
    data, cl_address = sock.recvfrom(1024)
    print(data.decode())
    sock.sendto('hello, client!'.encode(), cl_address)
```


#### client.py

```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_address = ('localhost', 8080)

sock.sendto('hello, server!'.encode(), serv_address)

data, _ = sock.recvfrom(1024)
print(data.decode())
sock.close()
```

Для успешного обмена данными сначала необходимо запустить серверный файл, который всегда готов 
слушать, а потом запустить клиентский файл, который сразу после установки соединения отправляет 
сообщение.

UDP соединение обеспечивается созданием UDP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`