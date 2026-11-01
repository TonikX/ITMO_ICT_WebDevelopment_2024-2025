
---

## 📄 `docs/task3.md` — HTTP, раздача HTML


# Задание 3. Раздача HTML-страницы по HTTP

## Постановка

Сервер при подключении клиента отдаёт HTTP-ответ с HTML-страницей из файла `index.html`.

**Требования:**
- Библиотека `socket`

## Архитектура

HTTP-ответ — текст в строгом формате: status line, заголовки, пустая строка, тело. Сервер читает `index.html`, считает длину в байтах для `Content-Length`, отправляет ответ.

## Файл `index.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой сервер</title>
</head>
<body>
    <h1>Привет от сокет-сервера!</h1>
    <p>Эта страница отдана через чистый socket.</p>
</body>
</html>
```

## Код сервера `sv_tk_3.py`

```python
import socket

HOST = "127.0.0.1"
PORT = 8080

def build_response(body: bytes) -> bytes:
    """Собирает HTTP-ответ по всем правилам."""
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Сервер запущен на http://{HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"Подключение от {client_addr}")

            try:
                request = client_sock.recv(4096)
                print("Запрос:")
                print(request.decode("utf-8", errors="replace"))

                with open("index.html", "rb") as f:
                    body = f.read()

                response = build_response(body)
                client_sock.sendall(response)
            finally:
                client_sock.close()
    except KeyboardInterrupt:
        print("\nОстановка сервера")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
```

## Результат
Открытие http://127.0.0.1:8080/ в браузере отображает HTML-страницу.

Ответ сервера
```text
Сервер запущен на http://127.0.0.1:8080
Подключение от ('127.0.0.1', 53606)
Запрос:
GET / HTTP/1.1
Host: 127.0.0.1:8080
Sec-Fetch-Dest: document
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0.1 Safari/605.1.15
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Accept-Language: ru
Priority: u=0, i
Accept-Encoding: gzip, deflate
Connection: keep-alive
```