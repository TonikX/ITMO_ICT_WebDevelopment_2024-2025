# Задание 2: TCP клиент-сервер

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.  

Требования:  
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола `TCP`.

Вариант 3 - поиск площади трапеции.  
Выполенена проверка на ввод чисел, их положительное значение без падения сервера.

## Файлы
- `tcp_server.py`: Реализация TCP сервера
```python
import socket


buffer_size = 1024
port = 8080
host = 'localhost'
server_address = (host, port)

def trapezoid_area(a, b, h):
    return (a + b) * h / 2

def check(x):
    if x <= 0:
        return False
    else: return True

def check_data(a, b, h):
    filtered = list(filter(check, [a, b, h]))
    if len(filtered) < 3:
        return False
    else:
        return True

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)

    # It defines the length of the backlog queue, which is the number of incoming connections that have been
    # completed by the TCP/IP stack but not yet accepted by the application.
    server_socket.listen(1)

    while True:
        print(f"TCP server has started on {host}:{port}")
        conn, client_address = server_socket.accept()

        print(f"Incoming connection from {client_address}")
        data = conn.recv(buffer_size).decode()
        if not data:
            break

        try:
            a, b, h = map(float, data.split())
            dq = check_data(a, b, h)
            if dq:
                result = trapezoid_area(a, b, h)
                conn.sendall(f"Trapezoid S = {result}\n".encode())
            else:
                conn.sendall("ERROR: Enter 3 POSITIVE numbers\n".encode())


        except ValueError:
            conn.sendall("ERROR: Enter 3 numbers\n".encode())

    server_socket.close()


if __name__ == "__main__":
    server()
```

- `tcp_client.py`: Реализация TCP клиента
```python
import socket

port = 8080
host = 'localhost'
server_address = (host, port)

a = input("Enter first base (a): ")
b = input("Enter second base (b): ")
h = input("Enter height (h): ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

client_socket.sendall(f"{a} {b} {h}".encode())

result = client_socket.recv(1024).decode()
print(f"{result}")

client_socket.close()
```
