# Задание 3:

## Описание задания
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html.`

## Требования
- Обязательно использовать библиотеку `socket`.

## Реализация

### Серверная часть
Сервер слушает входящие соединения, обрабатывает запросы и отправляет клиенту HTTP-ответ, содержащий HTML-страницу. Файл `index.html` используется для формирования содержимого страницы.

```python
import socket

HOST = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen()
html_content = open('index.html').read()

while True:
    client_connection, client_address = server_sock.accept()
    request = client_connection.recv(1024).decode()

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode())
```

### HTML-файл
HTML-страница, которую сервер отправляет клиенту, загружается из файла index.html

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Testing socket</h1>
</body>
</html>
```

## Пример запроса и ответа:
### HTTP-запрос от клиента:

```vbnet
GET /favicon.ico HTTP/1.1
Host: localhost:8080
Connection: keep-alive
sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36
sec-ch-ua-platform: "Windows"
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Referer: http://localhost:8080/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: ru,en;q=0.9
```

### HTTP-ответ от сервера:
```vbnet
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 150
Connection: close

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Testing socket</h1>
</body>
</html>
```