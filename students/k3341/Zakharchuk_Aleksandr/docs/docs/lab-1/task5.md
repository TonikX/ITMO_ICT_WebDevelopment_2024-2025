# Задание 5: Web-сервер для обработки GET и POST запросов

## Краткое описание задания

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Стек реализации

- Язык: Python
- Библиотека: socket
- Протокол: HTTP

## Как запускать

* Запустите сервер:

```bash
python server.py
```

* Для добавления данных используйте подготовленный скрипт:

```bash
python test.py
```

* Для просмотра данных откройте браузер и перейдите по адресу:

```bash
http://127.0.0.1:8080/
```

## Листинг кода

### data_structures.py

```python
import functools
import io
from urllib.parse import ParseResult, parse_qs, urlparse


class Request:
    def __init__(
            self,
            method: str,
            target: str,
            version: str,
            headers: dict[str, str],
            stream: io.BufferedReader,
        ):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.stream = stream

    def body(self) -> str:
        size = self.headers.get("Content-Length")
        if not size:
            return None
        return self.stream.read(int(size)).decode()

    @property
    def path(self) -> str:
        return self.url.path

    @property
    @functools.lru_cache(maxsize=None)
    def query(self) -> dict[str, str]:
        return parse_qs(self.url.query)

    @property
    @functools.lru_cache(maxsize=None)
    def url(self) -> ParseResult:
        return urlparse(self.target)


class Response:
    def __init__(
            self,
            status: str,
            reason: str,
            headers: dict[str, str] | None = None,
            body: str | None = None,
        ):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
  def __init__(self, status: str, reason: str, body: str | None = None):
    super()
    self.status = status
    self.reason = reason
    self.body = body
```

### server.py

```python
import http
import io
import socket
from email import message, parser

from data_structures import HTTPError, Response, Request

MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class HTTPServer:
    def __init__(self, host: str, port: int, max_connections: int = 10):
        self._host = host
        self._port = port
        self._max_connections = max_connections
        self._grades = {}

    def serve_forever(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        server_socket.settimeout(1)

        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen(self._max_connections)

            while True:
                try:
                    client_socket, address = server_socket.accept()
                    print(f"Client connected: {address}")

                    self.serve_client(client_socket)
                except TimeoutError:
                    continue
                except Exception as e:
                    print(f"Client serving failed: {e}")
        finally:
            server_socket.close()

    def serve_client(self, client_socket: socket.socket) -> None:
        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except Exception as e:
            self.send_error(client_socket, e)
        else:
            request.stream.close()
            client_socket.close()

    def parse_request_line(self, stream: io.BufferedReader) -> tuple[str, str, str]:
        raw_line = stream.readline(MAX_LINE + 1)
        if len(raw_line) > MAX_LINE:
            raise HTTPError(http.HTTPStatus.BAD_REQUEST, "Bad request", "Request line is too long")

        words = raw_line.decode("iso-8859-1").split()
        if len(words) != 3:
            raise HTTPError(http.HTTPStatus.BAD_REQUEST, "Bad request", "Malformed request line")

        method, target, version = words
        if version != "HTTP/1.1":
            raise HTTPError(
                http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED, "HTTP Version Not Supported",
            )

        return method, target, version

    def parse_request(self, client_socket: socket.socket) -> Request:
        request_stream = client_socket.makefile("rb")
        method, target, version = self.parse_request_line(request_stream)
        headers = self.parse_headers(request_stream)
        host = headers.get("Host")

        if not host:
            raise HTTPError(http.HTTPStatus.BAD_REQUEST, "Bad request", "Host header is missing")
        if host not in (self._host, f"{self._host}:{self._port}"):
            raise HTTPError(http.HTTPStatus.NOT_FOUND, "Not found")

        request = Request(
            method=method,
            target=target,
            version=version,
            headers=headers,
            stream=request_stream,
        )
        return request

    def parse_headers(self, stream: io.BufferedReader) -> message.Message:
        headers = []

        while True:
            line = stream.readline(MAX_LINE + 1)

            if len(line) > MAX_LINE:
                raise HTTPError(
                    http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                    "Request header too large",
                )

            if line in (b"\r\n", b"\n", b""):
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(
                    http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                    "Too many headers",
                )

        decoded_headers = b"".join(headers).decode("iso-8859-1")
        return parser.Parser().parsestr(decoded_headers)

    def handle_request(self, request: Request) -> Response:
        if request.path == "/" and request.method == http.HTTPMethod.POST:
            return self.handle_post(request)

        if request.path == "/" and request.method == http.HTTPMethod.GET:
            return self.handle_get()

        raise HTTPError(http.HTTPStatus.NOT_FOUND, "Not found")

    def handle_post(self, request: Request) -> Response:
        subject = request.query.get("subject")
        if subject is None:
            raise HTTPError(
                http.HTTPStatus.BAD_REQUEST,
                "Bad request",
                "No query param for subject",
            )

        grade = request.body()
        if grade is None:
            raise HTTPError(
                http.HTTPStatus.BAD_REQUEST,
                "Bad request",
                "Request body is empty",
            )

        self._grades.setdefault(subject[0], []).append(grade)

        response = Response(
            status=http.HTTPStatus.CREATED,
            reason="Created",
        )

        return response

    def handle_get(self) -> Response:
        html = "<html><body><h1>Grades</h1><ul>"

        for subject, grades in self._grades.items():
            html += f"<li>{subject}: {', '.join(grades)}</li>"

        html += "</ul></body></html>"

        response = Response(
            status=http.HTTPStatus.OK,
            reason="OK",
            headers={
                "Content-Type": "text/html",
                "Content-Length": str(len(html)),
            },
            body=html,
        )

        return response

    def send_response(self, client_socket: socket.socket, response: Response) -> None:
        response_stream = client_socket.makefile("wb")

        status_line = f"HTTP/1.1 {response.status} {response.reason}\n"
        response_stream.write(status_line.encode("iso-8859-1"))

        if response.headers:
            for key, value in response.headers.items():
                header_line = f"{key}: {value}\n"
                response_stream.write(header_line.encode("iso-8859-1"))

        response_stream.write(b"\n")

        if response.body:
            response_stream.write(response.body.encode())

        response_stream.flush()
        response_stream.close()

    def send_error(self, client_socket: socket.socket, error: HTTPError) -> None:
        try:
            status = error.status
            reason = error.reason
            body = (error.body or error.reason)
        except Exception:
            status = 500
            reason = b"Internal Server Error"
            body = b"Internal Server Error"

        response = Response(
            status=status,
            reason=reason,
            headers={"Content-Length": str(len(body))},
            body=body,
        )
        self.send_response(client_socket, response)


if __name__ == "__main__":
    server = HTTPServer(host="localhost", port=8080)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
```
