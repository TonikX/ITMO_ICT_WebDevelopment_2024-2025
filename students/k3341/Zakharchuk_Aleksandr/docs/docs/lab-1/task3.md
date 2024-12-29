# Задание 3: HTTP Сервер для выдачи HTML страницы

## Краткое описание задания

Реализовать серверную часть приложения, которая отвечает HTTP-сообщением, содержащим HTML-страницу из файла `index.html`.

## Стек реализации

- Язык: Python
- Библиотека: socket
- Протокол: HTTP

## Как запускать

* Запустите сервер:

```bash
python server.py
```

* Откройте браузер и перейдите по адресу:

```bash
http://localhost:12345/
```

## Листинг кода

### server.py

```python
import socket


def load_html_file(path: str) -> str:
    with open(path) as fi:
        html_data = fi.read()

    return html_data.strip()


def get_html_response(html_data: str) -> bytes:
    response_parts = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html\n",
        html_data,
    ]

    return "\n".join(response_parts).encode()


def main():
    html_data = load_html_file("index.html")
    html_response = get_html_response(html_data)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.bind(("localhost", 12345))
    conn.listen(10)

    while True:
        try:
            client, address = conn.accept()
            print(f"Подключился клиент {address}")

            request_data = client.recv(2048)
            print(f"Запрос клиента: {request_data.decode()}")

            client.send(html_response)
        except KeyboardInterrupt:
            print("Сервер остановлен")
            break
        finally:
            client.close()


if __name__ == "__main__":
    main()
```
