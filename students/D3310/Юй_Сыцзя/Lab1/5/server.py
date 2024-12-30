import socket

MAX_LINE = 64 * 1024

class MyHTTPServer:
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self._subjects = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen()
            print(f'Server started on http://{self.host}:{self.port}')
            while True:
                conn, _ = server.accept()
                with conn:
                    self.serve_client(conn)

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except Exception as e:
            self.send_error(conn, e)

    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, _ = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        return Request(method, target, headers, rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise ValueError('Request line too long')
        req_line = raw.decode('iso-8859-1').strip()
        method, target, version = req_line.split()
        if version != 'HTTP/1.1':
            raise ValueError('HTTP version not supported')
        return method, target, version

    def parse_headers(self, rfile):
        headers = {}
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if not line or line in (b"\r\n", b"\n"):
                break
            header = line.decode('iso-8859-1').strip()
            key, value = header.split(': ', 1)
            headers[key] = value
        return headers

    def handle_request(self, req):
        if req.method == 'GET':
            if req.path == '/':
                return self.handle_get_subjects()
            elif req.path.startswith('/subject/'):
                subject_id = req.path[len('/subject/'):]
                return self.handle_get_subject_by_id(subject_id)
        elif req.method == 'POST' and req.path == '/subject':
            return self.handle_post_subject(req)
        else:
            raise ValueError('Unsupported method')

    def handle_post_subject(self, req):
        content_length = int(req.headers.get('Content-Length', 0))
        body = req.rfile.read(content_length).decode('iso-8859-1')
        params = dict(param.split('=') for param in body.split('&'))

        if "name" not in params or 'mark' not in params:
            raise ValueError('The name and mark parameters are required')

        sub_id = len(self._subjects) + 1
        self._subjects[sub_id] = {
            "id": sub_id,
            "name": params.get('name'),
            "mark": params.get('mark')
        }
        return Response(201, "Created")

    def handle_get_subjects(self):
        html = "<html><head><title>Subjects</title></head><body><h1>Subjects</h1><ul>"
        for subject in self._subjects.values():
            html += f"<li>{subject['name']}: {subject['mark']}</li>"
        html += "</ul></body></html>"
        return Response(200, "OK", headers={"Content-Type": "text/html"}, body=html)

    def handle_get_subject_by_id(self, subject_id):
        try:
            subject_id = int(subject_id)
            subject = self._subjects.get(subject_id)
            if not subject:
                return Response(404, "Not Found", body="Subject not found")

            body = f"Name: {subject['name']}, Mark: {subject['mark']}"
            return Response(200, "OK", headers={"Content-Type": "text/plain"}, body=body)

        except ValueError:
            return Response(400, "Bad Request", body="Invalid subject ID")

    def send_response(self, conn, resp):
        status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
        conn.sendall(status_line.encode('iso-8859-1'))
        for header, value in (resp.headers or {}).items():
            conn.sendall(f"{header}: {value}\r\n".encode('iso-8859-1'))
        conn.sendall(b"\r\n")
        if resp.body:
            conn.sendall(resp.body.encode('iso-8859-1'))

    def send_error(self, conn, err):
        status_code = 500
        reason = "Internal Server Error"
        if isinstance(err, ValueError):
            status_code = 400
            reason = str(err)
        elif isinstance(err, Exception):
            reason = str(err)

        print(f"Error: {err}")

        status_line = f"HTTP/1.1 {status_code} {reason}\r\n"
        conn.sendall(status_line.encode('iso-8859-1'))
        conn.sendall(b"\r\n")
        conn.sendall(f"{reason}\r\n".encode('iso-8859-1'))


class Request:
    def __init__(self, method, target, headers, rfile):
        self.method = method
        self.path = target
        self.headers = headers
        self.rfile = rfile


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers or {}
        self.body = body


if __name__ == '__main__':
    server = MyHTTPServer()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
