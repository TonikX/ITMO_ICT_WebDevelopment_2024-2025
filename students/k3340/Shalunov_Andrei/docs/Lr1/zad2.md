# Задание 2:

## Описание задания
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Вариант операций:
4. Поиск площади параллелограмма.

## Требования
- Обязательно использовать библиотеку `socket`.
- Реализовать взаимодействие с помощью протокола TCP.

## Реализация

### Клиентская часть
Клиент запрашивает у пользователя длину основания и высоту параллелограмма, отправляет эти данные серверу и получает обратно результат вычисления.

```python
import socket

IP = 'localhost'
PORT = 8080

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((IP, PORT))

a = float(input('Длина: '))
h = float(input('Высота: '))
data = f'{a},{h}'
client_sock.send(data.encode())
response = client_sock.recv(1024).decode()
print(f'Площадь параллелограмма {response}')
client_sock.close()
```

### Серверная часть
Сервер принимает параметры параллелограмма (длина и высота), вычисляет площадь и отправляет результат обратно клиенту.

```python
import socket

IP = 'localhost'
PORT = 8080


def findSquare(a, h):
    return a * h

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, PORT))
server_sock.listen()

while True:
    connection, address = server_sock.accept()
    print(connection, address)
    data = connection.recv(1024).decode()
    a, h = map(float, data.split(','))
    connection.sendall(str(findSquare(a, h)).encode())
    connection.close()
```