import json
import socket


def get_input() -> tuple[int, int]:
    side1 = int(input("Введите длину первого катета (целое число): "))
    side2 = int(input("Введите длину второго катета (целое число): "))

    return side1, side2


def encode_request(side1: int, side2: int) -> bytes:
    params_dict = dict(side1=side1, side2=side2)
    json_string_params = json.dumps(params_dict)

    return json_string_params.encode()


def get_operation_result(side1: int, side2: int) -> float:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 12345))

    encoded_request = encode_request(side1, side2)
    conn.send(encoded_request)

    result = conn.recv(1024)

    return float(result.decode())


def main():
    try:
        side1, side2 = get_input()
    except ValueError:
        print("Ошибка во время ввода данных")
        return

    result = get_operation_result(side1, side2)
    print(f"Гипотенуза равна {result}")


if __name__ == "__main__":
    main()
