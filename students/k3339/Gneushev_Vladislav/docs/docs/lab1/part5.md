## Задание

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Как запустить

Зайти в папку `lab1/part5` и запустить командой `python server.py`


## Код

### Код клиента
```
import json
import socket
import threading

from constants import SERVER_HOST, SERVER_PORT
from dto import Request, DisciplineGrade
from schemas import CreateDisciplineScore

discipline_grades: list[DisciplineGrade] = []


class MyHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def serve_forever(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0
        )
        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Server is running on {self._host}:{self._port}")

            while True:
                conn, _ = serv_sock.accept()
                client_thread = threading.Thread(target=self.serve_client, args=(conn,))
                client_thread.daemon = True
                client_thread.start()

        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            data = conn.recv(1024).decode()
            if data:
                request = self.parse_request(data)
                self.handle_request(
                    request=request,
                    conn=conn
                )
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, data) -> Request:
        request_lines = data.split('\r\n')

        request_line = request_lines[0]
        method, uri, _ = request_line.split(' ', 2)

        headers = {}
        i = 1
        while request_lines[i] != '':
            header_key, header_value = request_lines[i].split(': ', 1)
            headers[header_key] = header_value
            i += 1

        body = '\r\n'.join(request_lines[i + 1:])

        return Request(
            path=uri,
            method=method,
            headers=headers,
            body=body
        )

    def handle_request(self, request: Request, conn: socket.socket):
        if request.method == 'POST':
            return self.handle_POST(
                request=request,
                conn=conn
            )
        elif request.method == 'GET':
            return self.handle_GET(
                conn=conn
            )

    def handle_POST(self, request: Request, conn: socket.socket):
        try:
            json_body = json.loads(request.body)
            body = CreateDisciplineScore(**json_body)
            discipline_grades.append(DisciplineGrade(
                discipline=body.discipline,
                grade=body.grade
            ))
        except json.JSONDecodeError:
            return self.send_error(conn, 'Invalid JSON')
        except Exception as e:
            return self.send_error(conn, e)
        self.send_response(conn, 'OK')

    def handle_GET(self, conn: socket.socket):
        data = """
        <html>
            <head>
                <title>Discipline grades</title>
            </head>
            <body>
                <h1>Discipline grades</h1>
                <table>
                    <tr>
                        <th>Discipline</th>
                        <th>Grade</th>
                    </tr>
        """
        for discipline_grade in discipline_grades:
            data += f"""
                    <tr>
                        <td>{discipline_grade.discipline}</td>
                        <td>{discipline_grade.grade}</td>
                    </tr>
            """
        data += """
                </table>
            </body>
        </html>
        """
        self.send_response(conn, data)

    def send_response(self, conn, resp):
        data = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/html; charset=utf-8",
            "",
            resp
        ]
        data = '\r\n'.join(data)
        conn.send(data.encode())

    def send_error(self, conn, err):
        self.send_response(conn, f'Error: {err}')


if __name__ == '__main__':
    serv = MyHTTPServer(
        host=SERVER_HOST,
        port=SERVER_PORT
    )
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
```

### Объекты для передачи данных (`DTO`)
```
from dataclasses import dataclass


@dataclass
class Request:
    path: str
    method: str
    headers: dict[str, str]
    body: str


@dataclass
class DisciplineGrade:
    discipline: str
    grade: int
```


### Схемы запросов
```
from dataclasses import dataclass


@dataclass
class CreateDisciplineScore:
    discipline: str
    grade: int
```