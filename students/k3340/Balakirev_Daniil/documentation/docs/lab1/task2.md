# Задание 2

## Текст задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции - теоремы Пифагора, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Требования

*   Обязательно использовать библиотеку `socket`.
*   Реализовать с помощью протокола TCP.

## Код

### client.py

    import socket

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1234))

    data = client.recv(1024)
    print(data.decode())

    user = input("Введите стороны a и b через пробел: ")
    client.send(user.encode())

    response = client.recv(1024)
    print(response.decode())

    client.close()

### server.py

    import socket

    def pifagor(a: int, b: int) -> float:
        return round((a**2 + b**2) ** (1/2))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1234))
    server.listen(1)
    print("Сервер запущен, ожидает подключения...")

    conn, addr = server.accept()
    print(f"Подключение от {addr}")
    conn.send("Теорема Пифагора".encode())

    data = conn.recv(1024)
    if data:
        a, b = map(int, data.decode().split())
        result = pifagor(a, b)
        conn.send(f'Гипотенуза: {result}'.encode())

    conn.close()