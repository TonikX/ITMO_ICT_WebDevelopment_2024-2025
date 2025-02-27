import socket
import json
import sys
from collections import defaultdict
from typing import Any


class MyHTTPServer:
    data = defaultdict(list)

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def serve_forever(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(10)
            s.settimeout(0.5)
            while True:
                try:
                    conn, address = s.accept()
                    with conn:
                        conn.settimeout(0.5)
                        try:
                            self.serve_client(conn)
                        except socket.timeout:
                            pass
                except socket.timeout:
                    pass

    def serve_client(self, conn: socket.socket) -> None:
        request = conn.recv(1024).decode()
        if request:
            method, path, version = self.parse_request(request)
            headers = self.parse_headers(request)

            if method == "GET":
                self.handle_get_request(path, conn)
            elif method == "POST":
                body = self.parse_body(request)
                self.handle_post_request(path, body, conn)

    @staticmethod
    def parse_request(request: str) -> tuple[str, str, str]:
        lines = request.split("\r\n")
        method, path, version = lines[0].split(" ")
        return method, path, version

    @staticmethod
    def parse_headers(request: str) -> dict[str, str]:
        lines = request.split("\r\n")
        headers = {}
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ")
            headers[key] = value
        return headers

    @staticmethod
    def parse_body(request: str) -> dict[Any]:
        lines = request.split("\r\n")
        i = lines.index("")
        if len(lines) > i + 1:
            body = "\r\n".join(lines[i + 1 :])
            return json.loads(body)
        return {}

    def handle_get_request(self, path: str, conn: socket.socket) -> None:
        if path == "/":
            with open("index.html", encoding="utf-8") as f:
                html_file = f.read()

            grades = "<br>".join(f"{discipline}: {', '.join(grades)}" for discipline, grades in self.data.items())
            html_file = html_file.replace("GRADES", grades)
            self.send_response(conn, html_file)
        else:
            with open("index.html", encoding="utf-8") as f:
                html_file = f.read()
            self.send_response(conn, html_file, status_code="404 Not Found")

    def handle_post_request(self, path: str, body: dict, conn: socket.socket) -> None:
        if path == "/":
            discipline = body.get("discipline", "")
            grade = body.get("grade", "")
            self.data[discipline].append(grade)

            self.send_response(conn, "")
        else:
            with open("index.html", encoding="utf-8") as f:
                html_file = f.read()
            self.send_response(conn, html_file, status_code="404 Not Found")

    @staticmethod
    def send_response(conn, response: str, status_code: str = "200 OK") -> None:
        response_headers = {
            "Content-Type": "text/html; charset=utf-8",
            "Connection": "close",
        }
        response_headers_raw = "".join(f"{k}: {v}\r\n" for k, v in response_headers.items())
        conn.sendall((f"""HTTP/1.1 {status_code}\r\n""" + response_headers_raw + "\r\n" + response).encode("utf-8"))


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit(1)
