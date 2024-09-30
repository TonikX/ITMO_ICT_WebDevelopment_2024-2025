## Задание №2. TCP-сервер

### Описание: 
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.
В качестве операции,окторую необходимо обработать и направить клиенту, (отталкиваясь от моего варианта) было предложено реализовать поиск площади трапеции.

### Требования:
* Обязательно использовать библиотеку socket. 
* Реализовать с помощью протокола TCP.

### Листинг кода:
#### server.py
```
import socket


def trapezoid_area(a_side, b_side, h_side):
    return (a_side + b_side)*h_side/2


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 1234))
    server_socket.listen()
    print("Server started")
    client_connection, client_address = server_socket.accept()
    with client_connection:
        client_message = client_connection.recv(1024).decode()
        a, b, h = client_message.split(',')
        client_connection.sendall(str(trapezoid_area(float(a), float(b), float(h))).encode())
        print("Client got the result")
```
#### client.py
``` 
import socket

a = input("Enter the first side (a): ")
b = input("Enter the second side (b): ")
h = input("Enter height (h): ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(("localhost", 1234))
    client_socket.sendall(f"{a}, {b}, {h}".encode())
    server_message = client_socket.recv(1024)

print(f"The area of the trapezoid: {server_message.decode()}")
```

### Пояснение:
В рамках данного задания был реализован простой TCP-сервер, при запуске которого после ввода всех необходимых параметров от клиента сервер обрабатывал данные, выполнял расчет площади и направлял готовый результат клиенту. При реализации используется потоковый сокет SOCK_STREAM, в основе которого лежит протокол TCP. Такие сокеты передают поток байтов, который может быть двунаправленным - т.е. приложение может и получать и отправлять данные.