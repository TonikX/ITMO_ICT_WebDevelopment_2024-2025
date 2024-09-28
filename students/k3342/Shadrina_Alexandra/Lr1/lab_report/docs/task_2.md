# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту. Реализовать с помощью протокола TCP.

## Реализация
Необходимо было создать клиент-серверное приложение для вычисления площади трапеции с использованием протокола TCP. Сервер принимает три параметра (длину оснований и высоту), вычисляет площадь с помощью функции и отправляет результат обратно клиенту. Клиент запрашивает ввод этих параметров у пользователя, отправляет их на сервер и выводит полученный ответ.
### Сервер
```python
import socket


def calculate_square(a, b, h):
    return (a + b) * h / 2


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    if not request:
        print('Данные не получены')
        client_connection.close()
        continue

    try:
        a, b, h = map(float, request.split(','))
        square = calculate_square(a, b, h)
        response = f'площадь трапеции {square}'
    except ValueError:
        response = 'Ошибка: некорректные данные.'

    print(f'Ответ: {response}')

    client_connection.sendall(response.encode())

    client_connection.close()

```
### Клиент
```python
import socket


def get_params():
    a = float(input("Длина первого основания (a): "))
    b = float(input("Длина второго основания (b): "))
    h = float(input("Высота (h): "))
    return a, b, h


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
a, b, h = get_params()

message = f'{a},{b},{h}'
client_socket.sendall(message.encode())

response = client_socket.recv(1024).decode()

if response:
    print(f'Ответ от сервера: {response}')
else:
    print('Ошибка: нет ответа от сервера')

client_socket.close()

```