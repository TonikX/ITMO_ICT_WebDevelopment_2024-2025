Задание:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Вариант операции:
Поиск площади параллелограмма.

Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

Листинг кода серверной части:
```
import socket

def area_parallelogram(a, h):
    return a * h

def check(x):
    if x <= 0:
        return False
    else: return True

def connection():
        host = '127.0.0.1'
        port = 5555

        server_socket = socket.socket()
        server_socket.bind((host, port))

        server_socket.listen()
        conn, addr = server_socket.accept()

        print('Соединение установлено с', addr)

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            a, h = map(int, data.split())
            result = area_parallelogram(a, h)
            conn.send(str(result).encode())
            print(f'Отправлен результат: {result}')

        conn.close()

if __name__ == "__main__":
    connection()

```

Листинг кода клиентской части:
```
import socket

def connection():
    host = '127.0.0.1'
    port = 5555

    client_socket = socket.socket()
    client_socket.connect((host, port))

    a = int(input("Введите длину стороны a: "))
    h = int(input("Введите высоту h: "))

    message = f"{a} {h}"
    client_socket.send(message.encode())

    result = client_socket.recv(1024).decode()
    print(f"Площадь параллелограмма: {result}")

    client_socket.close()

if __name__ == "__main__":
    connection()

```

Объяснение: При помощи протокола TCP(связь, отослать/принять сообщения), в клиентской части с консоли вводятся два значения.