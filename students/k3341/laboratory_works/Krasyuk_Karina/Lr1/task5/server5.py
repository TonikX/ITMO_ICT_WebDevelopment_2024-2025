import socket
from urllib.parse import parse_qs


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = {}

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        while True:
            client_socket, client_address = server_socket.accept()
            self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        if request:
            method, url, params = self.parse_request(request)
            self.handle_request(client_socket, method, url, params)

    def parse_request(self, data):
        headers, _, body = data.partition("\r\n\r\n")
        lines = headers.splitlines()

        request_line = lines[0]
        method, path, _ = request_line.split()

        params = None
        if method == 'POST':
            params = parse_qs(body)
        return method, path, params

    def handle_request(self, client_socket, method, url, params):
        if method == 'GET':
            self.handle_get(client_socket, url)
        elif method == 'POST':
            self.handle_post(client_socket, url, params)
        else:
            self.send_response(client_socket, 405, "Method Not Allowed")

    def handle_get(self, client_socket, url):
        if url == "/":
            self.send_grades_page(client_socket)
        else:
            self.send_response(client_socket, 404, "Not Found")

    def handle_post(self, client_socket, url, params):
        if url == "/":
            subject = params.get("subject", [""])[0]
            grade = params.get("grade", [""])[0]

            if subject == "" or grade == "":
                self.send_response(client_socket, 400, "Bad Request", "Missing subject or grade")
                return

            if subject in self.grades:
                self.grades[subject] += [grade]
            else:
                self.grades.update({subject: [grade]})
            self.send_response(client_socket, 200, "OK", "Grade submitted successfully")
        else:
            self.send_response(client_socket, 404, "Not Found")

    def send_grades_page(self, client_socket):
        if self.grades:
            content = "<h1>Оценки по дисциплинам</h1><ul>"
            for subject in self.grades:
                content += f"<li>{subject}: {' '.join(self.grades[subject])}</li>"
            content += "</ul>"
        else:
            content = "<h1>Нет записанных оценок.</h1>"

        self.send_response(client_socket, 200, "OK", content)

    def send_response(self, client_socket, status_code, status_message, content=""):
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += content
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()


if __name__ == "__main__":
    server = MyHTTPServer(host='localhost', port=8080)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
