import socket
import sys


class MyHTTPServer:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print(f'Server started on {self.host}:{self.port}')
            print("http://localhost:8080")

            while True:
                client_socket, client_address = server_socket.accept()
                self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        method, url, version = self.parse_request(request)
        headers, body = self.parse_headers(request)

        if method == 'GET':
            response_body = self.get_grades()
            self.send_response(client_socket, '200 OK', response_body)
        elif method == 'POST':
            self.add_grade(body)
            self.send_response(client_socket, '200 OK', '<html><body><h1>Grade Added</h1></body></html>')
        else:
            self.send_response(client_socket, '405 Method Not Allowed',
                               '<html><body><h1>Method Not Allowed</h1></body></html>')

    def parse_request(self, request):
        request_line = request.splitlines()[0]
        method, url, version = request_line.split(' ')
        return method, url, version

    def parse_headers(self, request):
        headers = {}
        lines = request.splitlines()
        body_index = request.index('\r\n\r\n') + 4
        headers_body = lines[1:]

        for line in headers_body:
            if line == '':
                break
            header, value = line.split(': ', 1)
            headers[header] = value

        body = request[body_index:]
        return headers, body

    def handle_request(self, method, url, body):
        if method == 'GET':
            return self.get_grades()
        elif method == 'POST':
            self.add_grade(body)
            return '<html><body><h1>Grade Added</h1></body></html>'
        else:
            return '<html><body><h1>Method Not Allowed</h1></body></html>'

    def get_grades(self):
        html_response = '<html><body><h1>Grades</h1><ul>'
        for discipline, grade in self.grades.items():
            html_response += f'<li>{discipline}: {grade}</li>'
        html_response += '</ul></body></html>'
        return html_response

    def add_grade(self, body):
        params = body.split('&')
        discipline = None
        grade = None
        for param in params:
            key, value = param.split('=')
            if key == 'discipline':
                discipline = value
            elif key == 'grade':
                grade = value
        if discipline and grade:
            self.grades[discipline] = grade

    def send_response(self, client_socket, status, body):
        response = f'HTTP/1.1 {status}\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}'
        client_socket.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    host = "localhost"
    port = 8080
    name = "GraduateWeb"
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass