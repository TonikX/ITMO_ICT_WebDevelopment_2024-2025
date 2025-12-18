import socket
from typing import Dict, List
from student_request import StudentRequest


class StudentHTTPServer:
    def __init__(self,
                 server_host: str = '127.0.0.1',
                 server_port: int = 8080) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.students: List[Dict[str, str]] = []

    def parse_headers(self, header_lines):
        headers = {}
        for line in header_lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value
        return headers

    def parse_request(self, data: str) -> StudentRequest:
        lines = data.split('\r\n')
        method, addr, version_proto = lines[0].split()
        empty_line_index = lines.index('')
        headers = self.parse_headers(lines[1:empty_line_index])
        body = '\r\n'.join(lines[empty_line_index + 1:])
        return StudentRequest(method, addr, version_proto, headers, body)

    def send_response(self, conn: socket.socket, body: str):
        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html; charset=utf-8\r\n'
            f'Content-Length: {len(body.encode())}\r\n'
            '\r\n'
            f'{body}'
        )
        conn.sendall(response.encode())

    def handle_request(self, request: StudentRequest, conn: socket.socket):
        if request.method == 'GET' and request.addr == '/':
            body = '''
<html>
<head>
    <meta charset="UTF-8">
    <title>Добавление студента</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #F7FAFC;
        }
        .container {
            width: 400px;
            margin: 80px auto;
            background: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #6EC1E4;
        }
        input {
            width: 100%;
            padding: 8px;
            margin-bottom: 12px;
            border-radius: 6px;
            border: 1px solid #CBD5E0;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #F4A6C1;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        a {
            display: block;
            margin-top: 12px;
            text-align: center;
            color: #6EC1E4;
            text-decoration: none;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Добавить студента</h1>
    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Имя" required>
        <input type="text" name="surname" placeholder="Фамилия" required>
        <input type="number" name="age" placeholder="Возраст" required>
        <button type="submit">Добавить</button>
    </form>
    <a href="/students">Посмотреть список студентов</a>
</div>

</body>
</html>
'''
            self.send_response(conn, body)

        elif request.method == 'POST' and request.addr == '/add':
            params = dict(
                p.split('=')
                for p in request.body.split('&')
                if '=' in p
            )
            self.students.append(params)
            self.send_response(
                conn,
                '<html><body><p>Студент добавлен</p><a href="/">Назад</a></body></html>'
            )

        elif request.method == 'GET' and request.addr == '/students':
            rows = ''.join(
                f'<tr><td>{s["name"]}</td><td>{s["surname"]}</td><td>{s["age"]}</td></tr>'
                for s in self.students
            )

            body = f'''
<html>
<head>
    <meta charset="UTF-8">
    <title>Список студентов</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #F7FAFC;
        }}
        .container {{
            width: 600px;
            margin: 60px auto;
            background: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            color: #6EC1E4;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }}
        th, td {{
            padding: 10px;
            border-bottom: 1px solid #E2E8F0;
            text-align: center;
        }}
        th {{
            background-color: #6EC1E4;
            color: #FFFFFF;
        }}
        a {{
            display: block;
            margin-top: 16px;
            text-align: center;
            color: #F4A6C1;
            text-decoration: none;
        }}
    </style>
</head>
<body>

<div class="container">
    <h1>Список студентов</h1>
    <table>
        <tr>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Возраст</th>
        </tr>
        {rows}
    </table>
    <a href="/">Добавить нового студента</a>
</div>

</body>
</html>
'''
            self.send_response(conn, body)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.server_host, self.server_port))
            server.listen(1)

            while True:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(4096).decode()
                    if data:
                        request = self.parse_request(data)
                        self.handle_request(request, conn)


if __name__ == '__main__':
    StudentHTTPServer().run()