### Условие
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

    Теорема Пифагора.
    Решение квадратного уравнения.
    Поиск площади трапеции.
    Поиск площади параллелограмма.

Требования:

    Обязательно использовать библиотеку socket.
    Реализовать с помощью протокола TCP.

Использованный вариант по списку -  поиск площади параллелограмма.
### 
Пример работы:
![](images/task2_0.jpg)
![](images/task2_1.jpg)

Листинг кода, client.py: 
``` py hl_lines="2 3"
import socket
from typing import Union


def check_data(data: str) -> Union[tuple[float, str], tuple[None, str]]:
    try:
        data = data.replace(',', '.')
        data = float(data)
        return data, 'ОК'
    except ValueError:
        return None, "Ошибка: введите число"


def connect():
    host = '127.0.0.1'
    port = 8080
    buffersize = 1024

    client_socket = socket.socket()
    client_socket.connect((host, port))

    print("Расчет площади параллелограмма")

    a = input("Введите длину основания a: ")
    a, code = check_data(a)
    if a is None:
        print(code)
    h = input("Введите длину высоты, проведенной к основанию h: ")
    h, code = check_data(h)
    if h is None:
        print(code)

    message = f"{a} {h}"
    client_socket.send(message.encode())

    result = client_socket.recv(buffersize).decode()
    print(f"Площадь параллелограмма: {result}")

    client_socket.close()


if __name__ == "__main__":
    connect()



```

server.py:
``` py hl_lines="2 3"
import socket
from typing import Tuple


def find_area(a: float, h: float, figure_len: int = 2) -> float:
    return round(a * h, figure_len)



def check_data(data: str) -> Tuple[float, float, str]:
    a, b = map(float, data.split())
    if a >= 0 and b >= 0:
        return a, b, 'ОК'
    else:
        return 0, 0, "Оба числа должны быть неотрицательными."


def connect():
    host = '127.0.0.1'
    port = 8080
    buffersize = 1024

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen()
    conn, _ = server_socket.accept()

    print("TCP server up and listening")

    while True:
        data = conn.recv(buffersize).decode()
        if not data:
            break
        a, h, status = check_data(data)
        if a is None:
            conn.send(status.encode())
        else:
            result = find_area(a, h)
            conn.send(str(result).encode())
            print(f'Ответ: {result}')

    conn.close()


if __name__ == "__main__":
    connect()


```