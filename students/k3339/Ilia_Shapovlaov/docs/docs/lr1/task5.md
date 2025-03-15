# Задание
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Сервер должен:

- Принять и записать информацию о дисциплине и оценке по дисциплине.

- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

## Примеры запросов с помощью curl:

- curl -X POST http://localhost:8080 -d "subject=Mathematics&grade=5"

- curl -X GET http://localhost:8080

## Сервер:
```py
import socket
import threading
from urllib.parse import parse_qs


class Server:
    def __init__(self, *, host: str, port: int, connections_queue_len: int = 5) -> None:
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._grades = {}

    def run(self):
        self._socket.bind((self._host, self._port))
        self._socket.listen(5)
        print("Server running on http://localhost:8080")

        while True:
            conn, addr = self._socket.accept()
            print(f"new connection from {addr}")

            threading.Thread(target=self._handle_request, args=(conn,)).start()

    def _handle_request(self, conn):
        request = conn.recv(1024).decode()
        headers = request.splitlines()

        if not headers:
            return

        method = headers[0].split()[0]

        response = None
        match method:
            case "POST":
                self._add_mark(request)
                response = 'HTTP/1.1 200 OK\n\nGrade added!'
            case "GET":
                response = self._get_marks()
            case _:
                response = 'HTTP/1.1 405 Method Not Allowed\n\n'

        conn.sendall(response.encode())
        conn.close()

    def _add_mark(self, request):
        body = request.splitlines()[-1]
        data = parse_qs(body)
        subject = data.get('subject', [''])[0]
        grade = data.get('grade', [''])[0]
        if subject and grade:
            self._grades[subject] = grade

    def _get_marks(self) -> str:
        response_body = '<html><body><h1>Grades</h1><ul>'
        for subject, grade in self._grades.items():
            response_body += f'<li>{subject}: {grade}</li>'
        response_body += '</ul></body></html>'
        return f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response_body}'


server = Server(host="127.0.0.1", port=8080)
server.run()
```
