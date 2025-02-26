# Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

```Площадь трапеции.```
### Требования:
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.
---
### server.py
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)


server_socket.listen(1)
print("Server is waiting for a client...")

while True:

    client_socket, client_address = server_socket.accept()
    print(f"Connected client with the address: {client_address}")

    try:

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Message from client: {data}")

        a, b, h = map(float, data.split(','))

        result = (a+b)/2 * h

        response_message = f"Area of the trapezium: {result}"
        client_socket.send(response_message.encode('utf-8'))

    except Exception as e:
        print(f"Error while calculating the response: {e}")

    finally:
        client_socket.close()
```
### client.py
```python
import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    print(f"To calculate the area of the trapezium input")
    a = float(input("Base a: "))
    b = float(input("Base b: "))
    h = float(input("Height h: "))

    message = f"{a},{b},{h}"
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

except Exception as e:
    print(f"Error while communicating with the server: {e}")

finally:
    client_socket.close()
```
