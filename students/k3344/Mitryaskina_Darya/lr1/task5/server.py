import socket
import sys
from email.parser import Parser

from exceptions import HTTPError
from utils import Request, Response
import json

MAX_LINE = 64 * 1024
MAX_HEADERS = 100

"""
# Добавление дисциплины
POST /subjects?name=ComputerScience

nc localhost 53210
POST /subjects?name=WebDevelopment HTTP/1.1
Host: example.local

POST /subjects?name=ComputerScience HTTP/1.1
Host: example.local
-------------------

# Добавление оценки
POST /subjects/123?mark=5

POST /subjects/1?mark=5 HTTP/1.1
Host: example.local

POST /subjects/1?mark=4 HTTP/1.1
Host: example.local

POST /subjects/2?mark=4 HTTP/1.1
Host: example.local
-------------------

# Получение оценок по дисциплине
GET /subjects/123

GET /subjects/1 HTTP/1.1
Host: example.local
Accept: text/html
-------------------

# Получение списка дисциплин
GET /subjects

GET /subjects HTTP/1.1
Host: example.local
Accept: text/html
Accept: application/json
"""
# py task5/server.py 127.0.0.1 53210 example.local
# python3 task5/server.py 127.0.0.1 53210 example.local


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._subjects = {}

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print("Client serving failed", e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        rfile = conn.makefile("rb")
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)

        host = headers.get("Host")
        if not host:
            raise HTTPError(400, "Bad request", "Host header is missing")
        if host not in (self._server_name, f"{self._server_name}:{self._port}"):
            raise HTTPError(404, "Not found")

        print(method, target, version, headers)
        return Request(method, target, version, headers, rfile)

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(400, "Bad request", "Request line is too long")

            if line in (b"\r\n", b"\n", b""):
                # завершаем чтение заголовков
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception("Too many headers")

        sheaders = b"".join(headers).decode("iso-8859-1")
        return Parser().parsestr(sheaders)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")

        req_line = str(raw, "iso-8859-1")
        req_line = req_line.rstrip("\r\n")
        words = req_line.split()
        if len(words) != 3:
            raise Exception("Malformed request line")

        method, target, version = words
        if version != "HTTP/1.1":
            raise Exception("Unexpected HTTP version")

        return method, target, version

    def handle_request(self, req):
        if req.path == "/subjects" and req.method == "POST":
            return self.handle_post_subject(req)

        if req.path.startswith("/subjects/"):
            subj_id = req.path[len("/subjects/") :]
            if subj_id.isdigit():
                if req.method == "GET":
                    return self.handle_get_marks(req, subj_id)
                if req.method == "POST":
                    return self.handle_add_mark(req, subj_id)

        if req.path == "/subjects" and req.method == "GET":
            return self.handle_get_subjects(req)

        raise HTTPError(404, "Not found")

    def handle_post_subject(self, req):
        subj_id = len(self._subjects) + 1
        self._subjects[subj_id] = {
            "id": subj_id,
            "name": req.query["name"][0],
            "marks": [],
        }
        return Response(204, "Created")

    def handle_get_marks(self, req, subj_id):
        subj = self._subjects.get(int(subj_id))
        if not subj:
            raise HTTPError(404, "Not found")

        accept = req.headers.get("Accept")
        if "text/html" in accept:
            contentType = "text/html; charset=utf-8"
            body = "<html><head></head><body>"
            body += f"<div>Оценки по дисциплине {subj['name']}:</div>"
            body += "<ul>"
            for u in subj["marks"]:
                body += f"<li>{u}</li>"
            body += "</ul>"
            body += "</body></html>"

        elif "application/json" in accept:
            contentType = "application/json; charset=utf-8"
            body = json.dumps(subj)

        else:
            return Response(406, "Not Acceptable")

        body = body.encode("utf-8")
        headers = [("Content-Type", contentType), ("Content-Length", len(body))]
        return Response(200, "OK", headers, body)

    def handle_add_mark(self, req, subj_id):
        mark = req.query.get("mark")[0]
        self._subjects[int(subj_id)]["marks"].append(mark)
        return Response(204, "Subject marks updated")

    def handle_get_subjects(self, req):
        accept = req.headers.get("Accept")
        if "text/html" in accept:
            contentType = "text/html; charset=utf-8"
            body = "<html><head></head><body>"
            body += f"<div>Дисциплины ({len(self._subjects)})</div>"
            body += "<ul>"
            for u in self._subjects.values():
                body += f'<li>#{u["id"]} {u["name"]}</li>'
            body += "</ul>"
            body += "</body></html>"

        elif "application/json" in accept:
            contentType = "application/json; charset=utf-8"
            body = json.dumps(self._subjects)

        else:
            return Response(406, "Not Acceptable")

        body = body.encode("utf-8")
        headers = [("Content-Type", contentType), ("Content-Length", len(body))]
        return Response(200, "OK", headers, body)

    def send_response(self, conn, resp):
        wfile = conn.makefile("wb")
        status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
        wfile.write(status_line.encode("iso-8859-1"))

        if resp.headers:
            for key, value in resp.headers:
                header_line = f"{key}: {value}\r\n"
                wfile.write(header_line.encode("iso-8859-1"))

        wfile.write(b"\r\n")

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode("utf-8")
        except:
            status = 500
            reason = b"Internal Server Error"
            body = b"Internal Server Error"
        resp = Response(status, reason, [("Content-Length", len(body))], body)
        self.send_response(conn, resp)


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
