import socket
from collections import defaultdict


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = defaultdict(list)

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Сервер запущен на http://{self.host}:{self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            self.serve_client(client_socket)

    def serve_client(self, client_socket):
        grades = client_socket.recv(1024).decode('utf-8')
        method, url, _ = self.parse_request(grades)

        if method == 'GET':
            response = self.handle_get_request(url)
        elif method == 'POST':
            response = self.handle_post_request(url, grades)

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def parse_request(self, request_data):
        lines = request_data.split('\n')
        method, url, version = lines[0].split()
        return method, url, version

    def parse_headers(self, request_data):
        lines = request_data.split('\n')
        headers = {}
        for line in lines[1:]:
            if line.strip():
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''
                headers[key] = value
        return headers

    def handle_get_request(self, url):
        if url == '/':
            return self.subject_html()
        else:
            return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

    def handle_post_request(self, url, grades):
        if url == '/add_grade':
            parameters = grades.split('\n')[-1]
            subject, grade = self.post_parse(parameters)
            self.grades[subject].append(grade)
            return self.subject_html()
        else:
            return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

    def post_parse(self, parameters):
        parameters = parameters.split('&')
        subject = None
        grade = None
        for param in parameters:
            key, value = param.split('=')
            if key == 'subject':
                subject = value
            elif key == 'grade':
                grade = value
        return subject, grade

    def subject_html(self):
        html = """\
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Оценки по дисциплине</title>
        </head>
        <body>
            <h1>Оценки по дисциплине</h1>
            <table style="border: solid black;">
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценка</th>
                    <th>Средний балл</th>
                </tr>
        """
        for subject, grades in self.grades.items():
            numeric_grades = [float(grade) for grade in grades]
            if numeric_grades:
                average_grade = sum(numeric_grades) / len(numeric_grades)
            else:
                average_grade = 0

            html += f"<tr><td>{subject}</td><td>{', '.join(grades)}</td><td>{average_grade:.2f}</td></tr>"

        html += """\
            </table>
            <h2>Добавить оценку</h2>
            <form method="post" action="/add_grade">
                <input type="text" id="subject" name="subject", placeholder="Предмет"><br>
                <input type="text" id="grade" name="grade", placeholder="Оценка"><br>
                <input type="submit" value="Добавить">
            </form>
        </body>
        </html>
        """
        return f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n{html}"


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 55555
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
