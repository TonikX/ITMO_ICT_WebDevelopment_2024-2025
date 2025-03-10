# Задание 2

## Суть задания
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

Теорема Пифагора.

### Клиент
Клиент запрашивает у пользователя катеты, отправляет их на сервер и печатает гипотенузу. Код клиента представлен ниже:
```python
import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 65432))  
    try:
        a = float(input("Введите длину первого катета: "))
        b = float(input("Введите длину второго катета: "))
        # Отправляем данные на сервер
        client_socket.send(f"{a},{b}".encode())

        # Получаем результат от сервера
        result = client_socket.recv(1024).decode()
        print(f"Результат от сервера: {result}")
    except ValueError:
        print("Ошибка: введены некорректные данные.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
```
### Сервер
Сервер принимает значения катетов от клиента, вычисляет гипотенузу и отправляет результат обратно. Код сервера представлен ниже:
```python
import socket
import math


def handle_client(client_socket):
    # Получаем данные от клиента
    data = client_socket.recv(1024).decode()
    try:
        a, b = map(float, data.split(","))
        c = math.sqrt(a ** 2 + b ** 2)
        result = f"Гипотенуза: {c:.2f}"
    except Exception as e:
        result = f"Ошибка обработки данных: {str(e)}"

    client_socket.send(result.encode())
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))  
    server_socket.listen(5)
    print("Сервер запущен и ожидает соединений...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключён клиент: {addr}")
        handle_client(client_socket)


if __name__ == "__main__":
    main()
```