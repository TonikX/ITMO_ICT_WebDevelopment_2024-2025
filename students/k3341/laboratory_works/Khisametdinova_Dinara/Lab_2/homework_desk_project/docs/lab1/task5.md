# Task 5

Необходимо написать простой web-сервер для обработки GET и POST http
запросов средствами Python и библиотеки socket.

Задание: сделать сервер, который может:

● Принять и записать информацию о дисциплине и оценке по дисциплине.

● Отдать информацию обо всех оценах по дсициплине в виде html-страницы.

plainhttp_server.py
```python
import socket
from urllib.parse import parse_qs

class SimpleHTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.data = {}  # для оценок

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Connection from {addr}")
                    self.handle_request(client_socket)

    def handle_request(self, client_socket):
        request = client_socket.recv(1024).decode()
        headers, body = request.split('\r\n\r\n', 1)
        request_line = headers.splitlines()[0]
        method, path, _ = request_line.split()

        if method == "GET":
            self.handle_get(client_socket, path)
        elif method == "POST":
            self.handle_post(client_socket, body)
        else:
            self.send_response(client_socket, "<h1>405 Method Not Allowed</h1>", "405 Method Not Allowed")

    def handle_get(self, client_socket, path):
        if path == "/grades":
            self.send_response(client_socket, self.render_grades_page(), "200 OK")
        else:
            self.send_response(client_socket, "<h1>404 Not Found</h1>", "404 Not Found")

    def handle_post(self, client_socket, body):
        params = self.parse_post_data(body)
        discipline = params.get('discipline', [''])[0]
        grade = params.get('grade', [''])[0]

        if discipline and grade:
            self.data[discipline] = grade  # сохранение оценки
            self.send_response(client_socket, "<h1>Grade Added</h1>", "200 OK")
        else:
            self.send_response(client_socket, "<h1>400 Bad Request</h1>", "400 Bad Request")

    def send_response(self, client_socket, content, status="200 OK"):
        response = f"HTTP/1.1 {status}\r\nContent-Type: text/html\r\n\r\n{content}"
        client_socket.sendall(response.encode())

    def render_grades_page(self):
        html = "<html><body><h1>Grades</h1><ul>"
        for discipline, grade in self.data.items():
            html += f"<li>{discipline}: {grade}</li>"
        html += "</ul></body></html>"
        return html

    def parse_post_data(self, body):
        return parse_qs(body)

if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start()

```
Testing

*Для отправки POST-запроса*

```bash
curl -X POST -d "discipline=Math&grade=5" http://localhost:8080
```
*Для получения списка оценок через GET:*

```bash
curl curl http://localhost:8080/grades
```