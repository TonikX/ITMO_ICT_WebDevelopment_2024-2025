# Задание №3: Раздача HTML-страницы по HTTP

## Постановка задачи

Реализовать серверную часть приложения.
Клиент подключается к серверу и в ответ получает HTTP-сообщение,
содержащее HTML-страницу, которую сервер подгружает из файла `index.html`.

Требования:

- [x] Обязательно использовать библиотеку socket

## Выполнение

### `index.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>HTTP-страница</title>
</head>
<body>
<h1>Привет, МИР!</h1>
<p>Эта страница загружена из файла <b>index.html</b>.</p>
</body>
</html>
```

Простой HTML-документ, который сервер будет отдавать по запросу.
Файл читается с диска и отправляется как тело HTTP-ответа.

### `server.py`

```python
import socket

SERVER_ADDR = ("", 9090)
INDEX_FILE = 'index.html'


def load_index_html():
    """Читает содержимое index.html из файла."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def build_http_response(body: str, status: str = "200 OK") -> bytes:
    """Формирует корректное HTTP-сообщение."""
    body_bytes = body.encode('utf-8')
    headers = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return headers.encode('utf-8') + body_bytes


def handle_client(sock, addr):
    data = sock.recv(1024)
    if not data:
        print(f"[*] Client {addr[0]}{addr[1]} disconnected")
        return

    request = data.decode("utf-8")
    first_line = request.split('\r\n')[0] if request else "(empty)"
    print(f"[Message from {addr[0]}:{addr[1]}] {first_line}")

    try:
        html = load_index_html()
        response = build_http_response(html)
    except FileNotFoundError:
        response = build_http_response("<h1>404 Not Found</h1>",
                                       status="404 Not Found")

    sock.sendall(response)


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

`SERVER_ADDR = ("", 9090)` — пустая строка в качестве адреса означает «слушать на всех доступных интерфейсах» (
`0.0.0.0`). Это позволяет подключаться к серверу не только с `localhost`, но и с других машин в сети.

`setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` — разрешает повторное использование адреса. Без этого после остановки сервера
порт `9090` остаётся в состоянии `TIME_WAIT`, и повторный `bind()` падает с ошибкой `Address already in use`.

`split('\r\n')[0]` — извлекает первую строку HTTP-запроса. HTTP-запрос начинается со строки вида `GET / HTTP/1.1`, и её
достаточно для логирования.

`load_index_html()` — открывает файл `index.html` в режиме чтения с кодировкой UTF-8 и возвращает его содержимое как
строку.

`build_http_response(body, status)` — собирает корректный HTTP-ответ:

- `HTTP/1.1 200 OK\r\n` — строка статуса;
- `Content-Type: text/html; charset=utf-8\r\n` — тип тела и кодировка;
- `Content-Length: {len(body_bytes)}\r\n` — длина тела в байтах (обязательный заголовок, чтобы клиент знал, когда
  прекратить чтение);
- `Connection: close\r\n` — указание закрыть соединение после ответа;
- `\r\n` — пустая строка, отделяющая заголовки от тела;
- тело ответа — байты HTML.

`FileNotFoundError` — обрабатывается, если файл `index.html` отсутствует. В этом случае клиенту отправляется страница с
кодом `404 Not Found`.

`sock.sendall(response)` — отправляет весь ответ целиком. В отличие от `send()`, `sendall()` гарантирует, что все байты
будут переданы (при необходимости выполняя несколько системных вызовов).

`ConnectionResetError` / `BrokenPipeError` — обрабатывают ситуации, когда клиент оборвал соединение до завершения
обмена.

`KeyboardInterrupt` / `finally` — корректное завершение по `Ctrl+C` с закрытием сокетов.

## Проверка

Запуск сервера:

```bash
$ python server.py
[*] TCP-server started on :9090
```

Запрос через `curl`:

```bash
$ curl -i http://localhost:9090/
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 179
Connection: close

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>HTTP-страница</title>
</head>
<body>
    <h1>Привет, МИР!</h1>
    <p>Эта страница загружена из файла <b>index.html</b>.</p>
</body>
</html>
```

Или открыть `http://localhost:9090/` в браузере — отобразится HTML-страница.

## Вывод

В ходе работы изучены принципы работы HTTP поверх TCP:

- `socket()` — создание TCP-сокета;
- `setsockopt()` — настройка повторного использования адреса;
- `bind()` — привязка к адресу;
- `listen()` — переход в режим прослушивания;
- `accept()` — приём входящего соединения;
- `recv()` — чтение HTTP-запроса;
- `sendall()` — отправка HTTP-ответа целиком;
- `close()` — освобождение сокета.

HTTP-ответ — обычный текст, оформленный по строгому формату: строка статуса, заголовки, пустая строка и тело.
Серверу достаточно прочитать содержимое `index.html`, посчитать его длину для заголовка `Content-Length` и отправить
всё одним пакетом через тот же сокет, что принял подключение.
