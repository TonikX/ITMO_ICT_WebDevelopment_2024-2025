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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen()
print("Сервер запущен на порту 8080...")
client_connection, client_address = server_socket.accept()
with client_connection:
    client_message = client_connection.recv(1024).decode()
    a, b, c = client_message.split(',')
    solve = (float(a) + float(b))*float(c)/2
    client_connection.sendall(str(solve).encode())
```
#### client.py
``` 
import socket

a, b, c = input("Введите коэффициент a: "), (input("Введите коэффициент b: ")), (input("Введите коэффициент c: "))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))
try:
    client_socket.send(f"{a}, {b}, {c}".encode())
    server_message = client_socket.recv(1024).decode()
    print(f"Результат: {server_message}")
finally:
    client_socket.close()
```

### Пояснение:
В рамках данного задания был реализован простой TCP-сервер, при запуске которого после ввода всех необходимых параметров от клиента сервер обрабатывал данные, выполнял расчет площади и направлял готовый результат клиенту. При реализации используется потоковый сокет SOCK_STREAM, в основе которого лежит протокол TCP. Такие сокеты передают поток байтов, который может быть двунаправленным - т.е. приложение может и получать и отправлять данные.