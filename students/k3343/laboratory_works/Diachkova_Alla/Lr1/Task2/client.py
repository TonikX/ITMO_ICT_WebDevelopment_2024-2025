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

