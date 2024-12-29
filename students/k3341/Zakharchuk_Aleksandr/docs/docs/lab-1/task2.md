# Задание 2: TCP Клиент-Сервер с математической операцией

## Краткое описание задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у сервера вычисление гипотенузы по теореме Пифагора, вводя стороны треугольника. Сервер обрабатывает запрос и возвращает результат.

## Стек реализации

- Язык: Python
- Библиотека: socket
- Протокол: TCP

## Как запускать

* Запустите сервер:

```bash
python server.py
```

* Запустите клиента:
```bash
python client.py
```

## Листинг кода

### client.py

```python
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
```

### server.py

```python
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
```
