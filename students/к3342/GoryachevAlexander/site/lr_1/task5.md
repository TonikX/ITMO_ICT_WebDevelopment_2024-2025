# Задание 5

## Суть  задания
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Задание:

Сервер должен:
Принять и записать информацию о дисциплине и оценке по дисциплине.
Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Сервер
```python
import socket
from urllib.parse import parse_qs, urlparse

class MyHTTPServer:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.data = {}

    def serve_forever(self):
        """Запуск сервера на сокете и обработка входящих соединений."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер {self.name} запущен на {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                self.serve_client(client_socket)

    def serve_client(self, client_socket):
        """Обработка клиентского подключения."""
        with client_socket:
            request = client_socket.recv(1024).decode()
            if not request:
                return

            method, path, headers, body = self.parse_request(request)
            response = self.handle_request(method, path, body)
            client_socket.sendall(response)

    def parse_request(self, request):
        """Обработка запроса: метод, URL, заголовки и тело."""
        lines = request.split("\r\n")
        method, path, _ = lines[0].split()
        headers = {}
        body = ""

        i = 1
        while lines[i]:
            key, value = lines[i].split(": ", 1)
            headers[key] = value
            i += 1

        if method == "POST":
            body = lines[-1]

        return method, path, headers, body

    def handle_request(self, method, path, body):
        """Обработка метода и маршрута запроса."""
        if method == "GET":
            return self.handle_get()
        elif method == "POST" and path == "/add":
            return self.handle_post(body)
        else:
            return self.send_response(404, "Not Found", "Страница не найдена")

    def handle_get(self):
        """Обработка GET-запроса: возврат всех дисциплин и оценок."""
        html = """
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Оценки по дисциплинам</title>
            </head>
            <body>
                <h1>Оценки по дисциплинам</h1>
                <ul>
        """
        for discipline, grade in self.data.items():
            html += f"<li>{discipline}: {grade}</li>"
        html += """
                </ul>
            </body>
        </html>
        """
        return self.send_response(200, "OK", html, content_type="text/html; charset=utf-8")

    def handle_post(self, body):
        """Обработка POST-запроса: добавление новой дисциплины и оценки."""
        params = parse_qs(body)
        discipline = params.get("discipline", [""])[0]
        grade = params.get("grade", [""])[0]

        if discipline and grade:
            self.data[discipline] = grade
            return self.send_response(200, "OK", "Данные успешно добавлены")
        else:
            return self.send_response(400, "Bad Request", "Некорректные данные")

    def send_response(self, status_code, reason, content, content_type="text/plain"):
        """Формирование и отправка ответа клиенту."""
        response = f"HTTP/1.1 {status_code} {reason}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content.encode())}\r\n"
        response += "\r\n"
        response += content
        return response.encode("utf-8")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    name = "WebServer"
    print("""Default post: curl -X POST -d "discipline=Math&grade=5" http://127.0.0.1:8080/add """)
    print("""Default get: curl http://127.0.0.1:8080""")

    server = MyHTTPServer(host, port, name)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
```