# Задание
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Требования:**

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.
 
***

# Решение

## Клиент

```python
import socket

HOST = 'localhost'
PORT = 9090


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print("Connected to server.")
    print("Solving quadratic equation ax² + bx + c = 0")

    user_input = input("Enter coefficients a b c (separated by space): ").strip()

    sock.sendall(user_input.encode("utf-8"))

    response = sock.recv(1024).decode("utf-8")

    print("\nResult from server:")
    print(response)

    sock.close()
    print("Connection closed.")


if __name__ == "__main__":
    main()

```

## Сервер

```python
import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print("Server started, waiting for connection...")

    conn, addr = sock.accept()
    print('Connected:', addr)

    data = conn.recv(1024).decode("utf-8").strip()
    print(f"Received: '{data}'")

    parts = data.split()
    if len(parts) != 3:
        response = "Error: exactly 3 numbers required (a b c)"
    else:
        try:
            a = float(parts[0])
            b = float(parts[1])
            c = float(parts[2])

            if a == 0:
                response = "Error: coefficient a cannot be zero"
            else:
                d = b ** 2 - 4 * a * c

                if d > 0:
                    x1 = (-b + d ** 0.5) / (2 * a)
                    x2 = (-b - d ** 0.5) / (2 * a)
                    response = f"Two real roots:\nx1 = {x1:.4f}\nx2 = {x2:.4f}"
                elif d == 0:
                    x = -b / (2 * a)
                    response = f"One real root:\nx = {x:.4f}"
                else:
                    response = f"No real roots\nD = {d:.4f}"

        except ValueError:
            response = "Error: all values must be numbers"

    conn.sendall(response.encode("utf-8"))
    print("Result sent. Closing connection.")

    conn.close()
    sock.close()


if __name__ == "__main__":
    main()
```

***

# Пояснение

Сервер на базе TCP-сокета (127.0.0.1:9090) в бесконечном цикле принимает соединения от клиентов.
Клиент передаёт три числа через пробел — длины оснований трапеции (a, b) и высоту (h).
Сервер проверяет корректность данных, вычисляет площадь по формуле S = (a + b) × h / 2, отправляет результат клиенту и закрывает соединение.
При ошибках (неверное количество чисел, некорректные значения, невозможность преобразования в float) возвращается соответствующее текстовое сообщение.

Клиент создает TCP сокет и пытается установить соединение с сервером на `127.0.0.1:9090`.
Далее он запрашивает данные от клиента с консоли и проводит их валидацию.
Если данные введены верно, то он отправляет их серверу, получает ответ и выводит ответ в консоль.