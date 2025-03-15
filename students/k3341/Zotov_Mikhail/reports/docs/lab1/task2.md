# Задание 2<br><br>

### Условие

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

#### Варианты операций:
1. Теорема Пифагора.
2. Решение квадратного уранвения.
3. Поиск площади трапеции.
4. Поиск площади параллелограмма.

#### Порядок выбора варианта:
Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

(Вариант 1)

---
### Код

#### Сервер
```python
import socket


def quadratic_equation_solver(a, b, c):
    d = b**2-4*a*c
    if d < 0:
        return 'This equation has no roots'
    elif d == 0:
        return f'{round((-b/(2*a)), 2)}'
    else:
        return f'{round((-b-d**0.5)/(2*a), 2)}, {round((-b+d**0.5)/(2*a), 2)}'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 2024))
sock.listen(0)
print("Server listening on port 2024")

while True:
    client_socket, client_address = sock.accept()
    print("Got connection from", client_address)

    while True:
        data = client_socket.recv(1024)
        if not data:
            print("Connection closed")
            break

        try:
            a, b, c = map(float, data.split())
            result = quadratic_equation_solver(a, b, c)
            client_socket.send(result.encode())
        except Exception as error:
            client_socket.send(f"This error occurred: {error}".encode())
```
#### Клиент
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2024)
sock.connect(server_address)

while True:
    message = input('Enter the coefficients of the equation (Enter to exit): ')
    if not message:
        break

    sock.send(message.encode())

    result = sock.recv(1024)
    print(result.decode())

sock.close()
```