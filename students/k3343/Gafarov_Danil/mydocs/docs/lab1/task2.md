# Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.
## Сервер
Листинг кода серверной части:
```python
import socket
from math import sqrt


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 8080
address = HOST, PORT
s.bind(address)
s.listen(1)
print("Server is running!")
while True:
    client_connection, client_address = s.accept()
    print("We got connection now")
    request = client_connection.recv(1024).decode()
    try:
        a, b = map(float, request.split(','))
        if a > 0 and b > 0:
            result = str(sqrt(a**2 + b**2))
        else:
            result = "Invalid data"
    except:
        result = "Invalid data"

# Отправили ответ
    client_connection.sendall(result.encode())
    client_connection.close()
```
## Клиент
Листинг кода клиентской части:
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Отправляем сообщение серверу
sides = input("Enter lengths of a and b: ")
client_socket.sendall(sides.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Server response: {response.decode()}')

# Закрываем соединение
client_socket.close()
```
## Объяснение
При помощи протокола TCP(связь, отослать/принять сообщения), в клиентской части с консоли вводятся два значения. Сервер обрабатывает операцию и возвращает результат.