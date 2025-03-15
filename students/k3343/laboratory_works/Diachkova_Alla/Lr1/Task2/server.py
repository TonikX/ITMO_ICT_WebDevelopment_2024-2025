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
