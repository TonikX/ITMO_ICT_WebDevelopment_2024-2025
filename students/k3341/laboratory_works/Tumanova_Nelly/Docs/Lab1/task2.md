# Задание №2: Вычисления через TCP

## Постановка задачи

Реализовать клиентскую и серверную часть приложения.
Клиент запрашивает выполнение математической операции,
параметры которой вводятся с клавиатуры.
Сервер обрабатывает данные и возвращает результат клиенту.

Вариант 3 — поиск площади трапеции.

Требования:

- [x] Обязательно использовать библиотеку socket
- [x] Реализовать с помощью протокола TCP

## Выполнение

### `server.py`

```python
import socket

SERVER_ADDR = ("localhost", 9090)


def calculate_trapezoid_area(a, b, h):
    return (a + b) * h / 2


def handle_client(sock, addr):
    data = sock.recv(1024)
    if not data:
        print(f"[*] Client {addr[0]}{addr[1]} disconnected")
        return

    request = data.decode("utf-8").strip()
    print(f"[Message from {addr[0]}:{addr[1]}] {request}")

    try:
        parts = request.split(";")
        if len(parts) != 3:
            raise ValueError("Expected three numbers separated by ';'")

        a = float(parts[0])
        b = float(parts[1])
        h = float(parts[2])

        area = calculate_trapezoid_area(a, b, h)
        response = f"The area of a trapezoid with bases {a}, {b} and height {h} = {area:.4f}"
    except ValueError as e:
        response = f"Error: {e}"

    sock.send(response.encode("utf-8"))


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # чтобы сразу после перезапуска сервера заново привязать его к тому же порту без ошибки
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen(socket.SOMAXCONN)

    print(f"[*] TCP-server started on {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Client {client_address[0]}{client_address[1]} connected")

            try:
                handle_client(client_socket, client_address)
            except (ConnectionResetError, BrokenPipeError) as e:
                print(f"[Error] {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("[*] TCP-server stopped")
    finally:
        server_socket.close()
```

`socket.socket(AF_INET, SOCK_STREAM)` — создаёт TCP-сокет для IPv4. `SOCK_STREAM` — потоковый сокет, обеспечивающий
надёжную доставку и порядок байт (в отличие от `SOCK_DGRAM` в UDP).

`setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` — разрешает повторное использование адреса. Без этого после остановки сервера
порт `9090` остаётся в состоянии `TIME_WAIT` несколько десятков секунд, и повторный `bind()` падает с ошибкой
`Address already in use`.

`bind(address)` — привязывает сокет к адресу `localhost:9090`.

`listen(SOMAXCONN)` — переводит сокет в режим прослушивания. `SOMAXCONN` — максимальный размер очереди входящих
соединений, задаваемый системой.

`accept()` — блокирующий вызов, извлекающий из очереди первое установленное соединение. Возвращает кортеж
`(client_socket, client_address)`, где `client_socket` — новый сокет именно для этого клиента, а `client_address` — его
адрес.

`recv(bufsize)` — читает до 1024 байт из сокета. Возвращает `b''` при разрыве соединения.

`decode('utf-8')` — превращает байты в строку.

`split(";")` — разбивает строку запроса `"a;b;h"` на три части. `float()` преобразует каждую часть в число.

`calculate_trapezoid_area(a, b, h)` — вычисляет площадь трапеции по формуле `(a + b) * h / 2`.

`send(data)` — отправляет ответ клиенту. `encode('utf-8')` превращает строку в байты.

`ConnectionResetError` / `BrokenPipeError` — обрабатывают ситуации, когда клиент оборвал соединение до завершения
обмена.

`KeyboardInterrupt` / `finally` — корректное завершение по `Ctrl+C` с закрытием сокетов.

### `client.py`

```python
import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    a = float(input("a = "))
    b = float(input("b = "))
    h = float(input("h = "))

    request = f"{a};{b};{h}"

    client_socket.settimeout(5.0)

    try:
        client_socket.connect(SERVER_ADDR)
        client_socket.send(request.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(f"[Message from {SERVER_ADDR[0]}:{SERVER_ADDR[1]}] {response}")
    except ConnectionRefusedError:
        print("[Error] Server is not available")
    except socket.timeout:
        print("[Error] Server timeout")
    finally:
        client_socket.close()
```

`socket.socket(AF_INET, SOCK_STREAM)` — создаёт TCP-сокет, как и на сервере.

`input()` / `float()` — считывает с клавиатуры три параметра трапеции и преобразует их в числа.

`f"{a};{b};{h}"` — формирует строку запроса, разделяя параметры точкой с запятой. Такой формат легко разобрать на
сервере через `split(";")`.

`settimeout(5.0)` — задаёт таймаут для блокирующих операций. Если сервер не отвечает, `connect()` или `recv()` выбросят
`socket.timeout`.

`connect(address)` — устанавливает TCP-соединение с сервером. Это ключевое отличие от UDP: перед обменом данными
выполняется трёхстороннее рукопожатие.

`send(data)` — отправляет запрос. `encode('utf-8')` превращает строку в байты.

`recv(bufsize)` — принимает ответ сервера.

`decode('utf-8')` — декодирует байты ответа в строку.

`ConnectionRefusedError` — выбрасывается, если сервер не запущен или отклонил соединение.

`close()` — закрывает сокет и освобождает ресурсы.

## Вывод

В ходе работы изучены базовые функции модуля `socket` для TCP:

- `socket()` — создание TCP-сокета;
- `setsockopt()` — настройка повторного использования адреса;
- `bind()` — привязка к адресу (сервер);
- `listen()` — переход в режим прослушивания (сервер);
- `accept()` — приём входящего соединения (сервер);
- `connect()` — установка соединения (клиент);
- `send()` / `recv()` — обмен данными;
- `settimeout()` — защита от бесконечного ожидания;
- `close()` — освобождение сокета.

TCP, в отличие от UDP, требует установления соединения перед обменом
данными и гарантирует доставку и порядок байт.
Дополнительные накладные расходы на установку соединения
окупаются надёжностью: параметры, введённые пользователем на клиенте,
дойдут до сервера, а результат вычисления — обратно.
