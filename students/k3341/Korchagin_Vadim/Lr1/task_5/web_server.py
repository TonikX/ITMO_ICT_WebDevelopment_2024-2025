import json
import socket
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


MAX_LINE = 64*1024
MAX_HEADERS = 100
class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._grades = {}

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen()

            while True:
                client_socket, _ = server_socket.accept()
                try:
                    self.serve_client(client_socket)
                except Exception as e:
                    print('Ошибка подключения клиента', e)
        finally:
            server_socket.close()

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

    def parse_request(self, client_socket):
        readfile = client_socket.makefile('rb')
        method, target, version = self.parse_request_line(readfile)
        headers = self.parse_headers(readfile)

        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        if host not in (self._server_name,
                        f'{self._server_name}:{self._port}'):
            raise HTTPError(404, 'Not found')

        return Request(method, target, version, headers, readfile)


    def parse_request_line(self, file):
        line = file.readline(MAX_LINE + 1)
        if len(line) > MAX_LINE:
            raise HTTPError(400, 'Bad request',
                            'Request line is too long')

        req_line = str(line, 'iso-8859-1')
        req_line = req_line.rstrip("\r\n")
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad request',
                            'Malformed request line')

        method, target, version = words
        if version != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')

        return method, target, version
    def parse_headers(self, file):
        headers = []

        while True:
            line = file.readline(MAX_LINE + 1)

            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')
            if line == (b"\r\n", b"\n", b" "):
                break

            headers.append(line)

            if len(headers) > MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')

        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)


    def handle_request(self, req):
        if req.path == '/grades' and req.method == 'POST':
            return self.handle_post_grades(req)

        if req.path == '/grades' and req.method == 'GET':
            return self.handle_get_grades(req)

        raise HTTPError(404, 'Not found')

    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason, [('Content-Length', len(body))], body)
        self.send_response(conn, resp)

    def handle_post_grades(self, req):
        # Извлечение данных из запроса
        data = req.query
        if 'subject' not in data or 'grade' not in data:
            raise HTTPError(400, 'Bad request', 'Missing subject or grade')

        subject = data['subject'][0]
        grade = data['grade'][0]

        # Добавляем дисциплину и оценку в хранилище
        self._grades[subject] = grade

        return Response(204, 'Created')

    def handle_get_grades(self, req):
        accept = req.headers.get('Accept')

        # Если клиент ожидает HTML-ответ
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head><title>Оценки</title></head><body>'
            body += '<h1>Оценки по дисциплинам</h1>'
            body += '<ul>'
            for subject, grade in self._grades.items():
                body += f'<li>{subject}: {grade}</li>'
            body += '</ul>'
            body += '</body></html>'

        # Если клиент ожидает JSON-ответ
        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            body = json.dumps(self._grades)

        else:
            # Если формат запроса неприемлем
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)


class Request:
    def __init__(self, method, target, version, headers, readfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.readfile = readfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers if headers is not None else []
        self.body = body


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super().__init__()
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 1234
    name = 'example.local'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
