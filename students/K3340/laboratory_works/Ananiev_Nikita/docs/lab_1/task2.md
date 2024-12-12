## Задание 2: Клиент-серверное взаимодейстие с помощью сокетов и TCP протокола (+ мат. задача)

Описание: <br> Реализовать клиентскую и серверную часть приложения. Клиент запрашивает усервера выполнение математической операции, параметры, которые вводятся склавиатуры. Сервер обрабатывает полученные данные и возвращает результатклиенту.

Код сервера: 
```python
import sys
import socket
import math

try:
    serv_socket = socket.socket()
    serv_socket.bind(('', 4242))
except socket.error:
    print('Failed to create socket')
    sys.exit()

max_conn_count, listening = 5, True

serv_socket.listen(max_conn_count)

while listening:
    client_socket, addr = serv_socket.accept()
    client_data = list(map(lambda x: int(x), client_socket.recv(1024).decode().split()))
    if not client_data or len(client_data) != 3:
        print("Invalid parameters for triangle area task")
        client_socket.close()
        break
    a, b, c = tuple(client_data)
    p = (a + b + c) / 2
    area = str(math.sqrt(p * (p - a) * (p - b) * (p - c)))
    client_socket.send(bytes(area, 'utf-8'))

```
Код клиента:

```python
import sys
import socket

try:
    client_sock = socket.socket()
except socket.error:
    print('Failed to create socket')
    sys.exit()


client_sock.connect(('localhost', 4242))
print("Please write the lengths of triangle sides:")
client_sock.send(bytes(input(), 'utf-8'))
res = client_sock.recv(1024)
print(f"Area = {res.decode()}")
client_sock.close()
```

*Примечание: среди вариантов не было теоремы Герона, но она показалась мне слегка нагляднее теоремы Пифагора*

