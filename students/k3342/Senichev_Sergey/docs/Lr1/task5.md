# Задание 5: Сервер для обработки оценок

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.    

Сервер должен:
- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## Файлы
- `server.py`: Реализация сервера
```python
import socket
from urllib.parse import parse_qs

class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self.host = host
        self.port = port
        self.server_name = server_name
        self.grades = {}

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Serving on {self.host}:{self.port}")

        while True:
            client_connection, client_address = server_socket.accept()
            self.serve_client(client_connection)

    def serve_client(self, client_connection):
        request = client_connection.recv(1024).decode()
        response = self.handle_request(request)
        client_connection.sendall(response.encode())
        client_connection.close()

    def handle_request(self, request):
        request_method = request.split()[0]
        request_path = request.split()[1]

        if request_method == 'GET':
            if request_path == '/grades':
                return self.get_grades()
        elif request_method == 'POST':
            if request_path == '/add_grade':
                body = request.split('\r\n\r\n', 1)[1]
                return self.add_grade(body)

        return self.send_response(404, 'Not Found', 'Page not found')

    def get_grades(self):
        grades_html = "<html><body><h1>Grades</h1><ul>"
        for subject, grade in self.grades.items():
            grades_html += f"<li>{subject}: {grade}</li>"
        grades_html += "</ul></body></html>"
        return self.send_response(200, 'OK', grades_html, 'text/html')

    def add_grade(self, body):
        params = parse_qs(body)
        subject = params.get('subject', [''])[0]
        grade = params.get('grade', [''])[0]

        if subject and grade:
            self.grades[subject] = grade
            return self.send_response(200, 'OK', 'Grade added successfully\n')
        else:
            return self.send_response(400, 'Bad Request', 'Invalid parameters\n')

    def send_response(self, status_code, status_text, body, content_type='text/plain'):
        response = f'HTTP/1.1 {status_code} {status_text}\r\n'
        response += f'Content-Type: {content_type}\r\n'
        response += f'Content-Length: {len(body)}\r\n'
        response += '\r\n'
        response += body
        return response

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    server_name = 'GradesServer'
    serv = MyHTTPServer(host, port, server_name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```
