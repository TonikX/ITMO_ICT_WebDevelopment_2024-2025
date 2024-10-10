import socket
from urllib.parse import urlparse, parse_qs


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер запущен на {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Подключение от {addr}")
                    self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request_data = client_socket.recv(1024).decode('utf-8')
        if not request_data:
            return

        method, url, headers, body = self.parse_request(request_data)
        print(f"Метод: {method}, URL: {url}")

        if method == "GET":
            self.handle_get(client_socket)
        elif method == "POST":
            self.handle_post(client_socket, body)

    def parse_request(self, request_data):
        request_lines = request_data.split("\r\n")
        method, url, protocol = request_lines[0].split(" ")
        headers = {}
        body = ""

        i = 1
        while request_lines[i]:
            header_name, header_value = request_lines[i].split(": ", 1)
            headers[header_name] = header_value
            i += 1

        if "Content-Length" in headers:
            content_length = int(headers["Content-Length"])
            body = request_lines[-1][:content_length]

        return method, url, headers, body

    def handle_get(self, client_socket):
        response_body = open("index.html", encoding="utf-8").read()

        grades = ("<table class='table'>"
                  "<thead>"
                      "<tr>"
                          "<th scope='col'>Дисциплина</th>"
                          "<th scope='col'>Оценки</th>"
                      "</tr>"
                  "</thead><tbody>")
        for subject, grade in self.grades.items():
            grades += f"<tr><td>{subject}</td><td>"
            for _grade in grade:
                grades += f"<span class='m-1 badge text-bg-success'>{_grade}</span>"
            grades += "</td></tr>"
        if len(self.grades) == 0:
            grades += f"<tr><td>Данных пока нет :(</td><td></td></tr>"
        grades += "</tbody></table>"

        response_body = response_body.replace("%GRADES%", grades)

        self.send_response(client_socket, "200 OK", response_body)

    def handle_post(self, client_socket, body):
        params = parse_qs(body)
        subject = params.get('subject', [''])[0]
        grade = params.get('grade', [''])[0]

        if subject and grade:
            if subject in self.grades.keys():
                self.grades[subject].append(grade)
            else:
                self.grades[subject] = [grade]
            self.handle_get(client_socket)
        else:
            self.send_response(client_socket, "400 Bad Request", "Ошибка: отсутствуют необходимые параметры")

    def send_response(self, client_socket, status, body):
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.sendall(response.encode('utf-8'))


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    server = MyHTTPServer(host, port)
    server.serve_forever()