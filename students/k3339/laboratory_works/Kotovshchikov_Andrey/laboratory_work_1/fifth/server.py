from io import BufferedReader
import socket
import re
import sys

from event_loop import EventLoop, TaskType
from exception import ServerExeption
from response import Response
from request import Request
from routes import get_all_subjects, save_subject

type Socket = socket.socket


class HTTPServer:
    _max_line: int = 64 * 1024
    _max_headers: int = 100
    _host: str
    _port: int

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    def serve_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self._host, self._port))
            server.listen()
            while True:
                yield (TaskType.TO_READ, server)
                connection, _ = server.accept()

                try:
                    event_loop.create_task(self.serve_client(connection))
                except Exception as exc:
                    print(exc)
        finally:
            server.close()

    def serve_client(self, connection: Socket):
        try:
            yield (TaskType.TO_READ, connection)
            request = self.parse_request(connection)
            response = self.handle_request(request)

            yield (TaskType.TO_WRITE, connection)
            self.send_response(connection, response)

        except ServerExeption as exc:
            print(exc)
            error_response = Response(status_code=exc.status_code, reason=exc.reason)
            self.send_response(connection, error_response)

        except Exception as exc:
            print(exc)
            error_response = Response(status_code=500, reason="Internal Server Error")
            self.send_response(connection, error_response)

        finally:
            connection.close()

    def parse_request(self, connection: Socket):
        stream = connection.makefile("rb")
        raw = stream.readline(self._max_line + 1)
        if len(raw) > self._max_line:
            raise ServerExeption(431, "Too long request line")

        line = raw.decode("iso-8859-1").rstrip("\r\n")
        line_parts = line.split()
        if len(line_parts) != 3:
            raise ServerExeption(400, "Malformed request line")

        method, url, version = line_parts
        headers = self.parse_headers(stream)

        return Request(
            method=method,
            url=url,
            version=version,
            stream=stream,
            headers=headers,
        )

    def parse_headers(self, stream: BufferedReader):
        headers = dict()
        while True:
            line = stream.readline(self._max_line + 1)
            if len(line) > self._max_line:
                raise ServerExeption(431, "Too long header line")

            if line in (b"\r\n", b"\n", b""):
                break

            header, value = line.decode("iso-8859-1").split(":", 1)
            headers[header] = value.rstrip("\r\n")
            if len(headers) > self._max_headers:
                raise ServerExeption(431, "Too many headers")

        return headers

    def handle_request(self, request: Request):
        if not re.fullmatch(r"\/subjects\/\d+", request.path):
            raise ServerExeption(404, "Not found")

        student_id = request.path[len("/subjects/") :]
        response = None
        if request.method == "GET":
            response = get_all_subjects(request=request, student_id=int(student_id))

        elif request.method == "POST":
            response = save_subject(request=request, student_id=int(student_id))

        if response is None:
            raise ServerExeption(405, "Method not allowed")

        return response

    def send_response(self, connection: Socket, response: Response):
        stream = connection.makefile("wb")
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
        stream.write(status_line.encode("iso-8859-1"))

        if response.headers:
            for key, value in response.headers.items():
                header_line = f"{key}: {value}\r\n"
                stream.write(header_line.encode("iso-8859-1"))

        stream.write(b"\r\n")
        if response.body is not None:
            stream.write(response.body)

        stream.flush()
        stream.close()


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    server = HTTPServer(host, port)
    try:
        event_loop = EventLoop(main=server.serve_forever())
        event_loop.run()
    except KeyboardInterrupt:
        pass
