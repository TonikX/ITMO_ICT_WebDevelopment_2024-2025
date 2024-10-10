# Лабораторная 1, Задание 5
## Условие
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.
### Требования:
Сервер должен:

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
  
## Решение

`HTTPserver.py`
```
import socket
from threading import Thread
from HTTPRequest import HTTPRequest
from HTTPResponse import HTTPResponse
from Course import Course
from CourseRepository import CourseRepository


"""
GET /courses/
POST /courses/ 
name=&grade=
"""


class HTTPServer:
    def __init__(self, host="localhost", port=1234):
        self._host = host
        self._port = port
        self._course_repo = CourseRepository()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            print(f"Listening on {self._host}:{self._port}")

            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    client_thread = Thread(
                        target=self.serve_client, args=(client_socket,)
                    )
                    client_thread.start()
                except Exception as e:
                    print("Client serving failed: ", e)
        finally:
            print("Server is shutting down..")
            server_socket.close()

    def serve_client(self, client_socket: socket.socket):
        try:
            data = self.recvall(client_socket)
            print(f"Received:\n{data}")
            request = HTTPRequest(data)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except Exception as e:
            self.send_error(client_socket, e)
        finally:
            client_socket.close()

    def recvall(self, client_socket: socket.socket):
        data = b""
        while True:
            chunk = client_socket.recv(4096)
            data += chunk
            if not chunk:
                break
            if b"\r\n\r\n" in data:
                break
        return data.decode()

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        match request.path:
            case "/courses":
                match request.method:
                    case "GET":
                        courses = self._course_repo.get_courses()
                        body = self.get_html_courses(courses)
                        return HTTPResponse(200, "OK", body=body)
                    case "POST":
                        body = request.body
                        if body:
                            params = dict(pair.split("=") for pair in body.split("&"))
                            name = params.get("name", "")
                            grade = params.get("grade", "")
                            if name and grade:
                                self._course_repo.insert_course(
                                    name=name, grade=int(grade)
                                )
                                return HTTPResponse(201, "Created")
                        return HTTPResponse(400, "Bad Request")
                    case _:
                        return HTTPResponse(404, "Not Found")
            case _:
                return HTTPResponse(404, "Not Found")

    def send_response(self, client_socket: socket.socket, response: HTTPResponse):
        response_str = response.get_response_str()
        client_socket.sendall(response_str.encode())
        print(f"Sent:\n{response_str}")

    def send_error(self, client_socket: socket.socket, err: Exception):
        status = 500
        status_text = "Internal Server Error"
        body = str(err)
        print(f"Error: {body}")
        response = HTTPResponse(status, status_text, body=body)
        self.send_response(client_socket, response)

    def get_html_courses(self, courses: list[Course]):
        html = "<html><head><title>Courses</title></head><body>"

        html += "<h1>Courses</h1>"
        if courses:
            html += "<ul>"
            for course in courses:
                html += f"<li>ID: {course.id}, Name: {course.name},\
                  Grade: {course.grade}</li>"
            html += "</ul>"
        else:
            html += "<p>No courses available.</p>"
        html += "</body></html>"
        return html


if __name__ == "__main__":
    host = "localhost"
    port = 1234
    server = HTTPServer(host, port)
    server.run()

```
`HTTPRequest.py`
```
from typing import Any


class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.path = None
        self.query_params: dict[str, Any] | None = None
        self.version = "HTTP/1.1"
        self.headers: dict[str, str] = dict()
        self.body: str | None = None

        self.parse(data)

    def parse(self, data: str):
        lines = data.splitlines()
        request_line = lines[0]
        words = request_line.split()
        if len(words) != 3:
            raise Exception("Malformed request line")

        self.method, self.uri, self.version = words
        self.parse_uri()

        if self.version != "HTTP/1.1":
            raise Exception("Unexpected HTTP version")

        for line in lines[1:]:
            if line.strip() == "":
                break
            key, value = line.split(":", 1)
            self.headers[key.strip()] = value.strip()

        body_start_index = lines.index("") + 1
        self.body = "\n".join(lines[body_start_index:])

    def parse_uri(self):
        if not self.uri:
            return Exception("Invalid URI")
        if "?" in self.uri:
            self.path, query = self.uri.split("?", 1)
            self.parse_query(query)
        else:
            self.path = self.uri

    def parse_query(self, query: str):
        if not query:
            self.query_params = None
            return
        self.query_params = dict()
        for param in query.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                self.query_params[key] = value
            else:
                self.query_params[param] = None

```

`HTTPResponse.py`
```
class HTTPResponse:
    def __init__(self, status, status_text, headers=None, body=None):
        self.status = status
        self.status_text = status_text
        self.headers = headers
        self.body: str | None = body
        self.version = "HTTP/1.1"

    def get_response_str(self) -> str:
        response = ""
        status_line = f"{self.version} {self.status} {self.status_text}\r\n"
        response += status_line

        if self.headers:
            for key, value in self.headers:
                header_line = f"{key}: {value}\r\n"
                response += header_line
        else:
            headers = "Content-Type: text/html; charset=utf-8\r\n"
            headers += (
                f"Content-Length: {len(self.body.encode()) if self.body else 0}\r\n"
            )
            response += headers
        response += "\r\n"

        if self.body:
            response += self.body

        return response

```

`Course.py`
```
from dataclasses import dataclass


@dataclass
class Course:
    id: int
    name: str
    grade: int

```
`CourseRepository.py`
```
from Course import Course


class CourseRepository:
    def __init__(self):
        self.courses: list[Course] = []

    def get_courses(self) -> list[Course]:
        return self.courses

    def insert_course(self, name: str, grade: int):
        id = len(self.courses) + 1
        if grade < 0:
            raise Exception("Grade must not be negative.")
        course = Course(id, name, grade)
        self.courses.append(course)

```

### Запуск

**GET /courses** - получить все курсы
```bash
$ curl localhost:1234/courses -i
```
**POST /courses** - создать новый курс с именем и оценкой
```bash
$ curl localhost:1234/courses -d name=WEB\&grade=5 -i
```