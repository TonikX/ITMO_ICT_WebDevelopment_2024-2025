import json
import math
import socket


def decode_request(encoded_request: bytes) -> tuple[int, int]:
    string_request = encoded_request.decode()
    params_dict = json.loads(string_request)

    return params_dict["side1"], params_dict["side2"]


def calculate_area(side1: int, side2: int) -> int:
    return math.sqrt(side1**2 + side2**2)


def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.bind(("localhost", 12345))
    conn.listen(10)

    while True:
        try:
            client, address = conn.accept()
            print(f"Клиент {address} подключился")

            data = client.recv(1024)
            side1, side2 = decode_request(data)
            result = calculate_area(side1, side2)

            client.send(str(result).encode())
        except KeyboardInterrupt:
            print("Сервер остановлен")
            conn.close()
            break


if __name__ == "__main__":
    main()
