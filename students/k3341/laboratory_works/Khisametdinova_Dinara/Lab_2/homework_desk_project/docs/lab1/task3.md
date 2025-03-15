# Task 3

Реализовать серверную часть приложения. Клиент подключается к серверу. В ответ
клиент получает http-сообщение, содержащее html-страницу, которую сервер
подгружает из файла index.html.

http_server.py
```python
import os
from server import Server

class HTTPServer(Server):
    def send_html_response(self):
        data, conn = self.handle_client()

        html_file = 'index.html'
        if os.path.exists(html_file):
            with open(html_file, 'r') as file:
                html_content = file.read()
        else:
            html_content = "<h1>404 Not Found</h1>"

        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"

        conn.sendall(http_response.encode())
        print("Sent HTML page to client")

        conn.close()

if __name__ == "__main__":
    server = HTTPServer(protocol_type="TCP")
    print("HTTP Server is running...")
    server.send_html_response()
    server.close()

```
index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Page</title>
</head>
<body>
    <h1>Hey, I'm Dinara</h1>
    <p>I enjoy Valheim.</p>
</body>
</html>
```
