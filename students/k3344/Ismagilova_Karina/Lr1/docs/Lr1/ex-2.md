## Задание № 2:
Реализовать клиентскую и серверную часть приложения. 
Клиент запрашивает выполнение математической операции, параметры 
которой вводятся с клавиатуры. Сервер обрабатывает 
данные и возвращает результат клиенту.  
Моё задание по варианту - реализовать теорему Пифагора

### Стэк реализации:  
- Язык - Python
- Библиотеки - socket, math
- Протокол - TCP

### Запуск программ:
Сервер:
```bash
    python server.py
```
Клиент:
```bash
    python client.py
```

### Листинг кода:

Сервер:
```python
import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Сервер запущен")

def hypotenuse_calc(a, b):
    return math.sqrt(a**2 + b**2)

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    triangle = client_connection.recv(1024).decode()
    a, b = map(float, triangle.split())
    hypotenuse = hypotenuse_calc(a, b)
    response = f"Гипотенуза: {hypotenuse:.2f}"

    client_connection.send(response.encode())
    # client_connection.close()
```
Клиент:
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

a = input("Длина первого катета: ")
b = input("Длина второго катета: ")

client_socket.send(f"{a} {b}".encode())

response = client_socket.recv(1024)
print(f'Ответ: {response.decode()}')

client_socket.close()
```