### Задание 2:

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение теоремы 
Пифагора, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Требования:

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

### Ход работы:

#### server.py

```
import socket
import math

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen(1)

print('connected:', serv_address)

while True:

    conn, cl_address = serv_sock.accept()

    try:
        data = conn.recv(1024).decode()
        a, b = map(float, data.split())
        if a <= 0 or b <= 0:
            conn.send('the sides cannot be negative or equal zero'.encode())
        hypotenuse = math.sqrt(a**2 + b**2)
        conn.send(f'length of hypotenuse = {hypotenuse}'.encode())
    finally:
        conn.close()
```


#### client.py

```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
sock.connect(serv_address)

try:
    a = input('length of side a: ')
    b = input('length of side b: ')
    sock.sendall(f'{a} {b}'.encode())

    data = sock.recv(1024).decode()
    print(data)

finally:
    sock.close()
```

Для успешного обмена данными сначала необходимо запустить серверный файл, который всегда готов 
слушать, а затем клиентский файл, который сразу после установки соединения отправляет стороны 
треугольника. Сервер принимает стороны треугольника и выполняет поиск гипотенузы, предварительно 
проверив положительность сторон.

TCP соединение обеспечивается созданием TCP-socket с помощью параметра `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`