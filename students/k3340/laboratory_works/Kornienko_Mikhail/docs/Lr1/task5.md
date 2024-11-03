# Задание 5

## Описание

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: HTTP

## Как запускать

1. Сервер:

   Листинг:
```python
import socket
import threading
from urllib.parse import unquote


class GradeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_sock, _ = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock,)).start()

    def handle_client(self, client_sock):
        try:
            request = client_sock.recv(1024).decode()
            headers, body = self.parse_request(request)
            method = headers[0].split(' ')[0]

            print(f"Received {method} request")

            if method == 'GET':
                self.handle_get(client_sock)
            elif method == 'POST':
                self.handle_post(client_sock, body)

        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            client_sock.close()

    @staticmethod
    def parse_request(request):
        parts = request.split('\r\n\r\n')
        headers = parts[0].split('\r\n')
        body = parts[1] if len(parts) > 1 else ''
        return headers, body

    def handle_get(self, client_sock):
        response_body = self.generate_html()
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(response_body)}

{response_body}"""
        client_sock.sendall(response.encode())

    def handle_post(self, client_sock, body):
        params = self.parse_post_data(body)
        discipline = params.get('discipline', '')
        grade = params.get('grade', '')

        if discipline and grade:
            existing = next((item for item in self.grades if item['discipline'] == discipline), None)
            if existing:
                existing['grade'] += f", {grade}"
            else:
                self.grades.append({'discipline': discipline, 'grade': grade})

        response_body = 'Data received'
        response = f"""HTTP/1.1 200 OK
Content-Type: text/plain

{response_body}"""
        client_sock.sendall(response.encode())

    def generate_html(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>LR1</title>
</head>
<body>
    <h1>Practice work 1</h1>
    <h2>Grades</h1>
    <table border="1">
        <tr><th>Discipline</th><th>Grade</th></tr>"""

        for entry in self.grades:
            html += f"<tr><td>{entry['discipline']}</td><td>{entry['grade']}</td></tr>"

        html += """
    </table>
    <a>Done by Kornienko Mikhail</a>
</body>
</html>"""
        return html

    @staticmethod
    def parse_post_data(data):
        params = {}
        pairs = data.split('&')
        for pair in pairs:
            key, value = pair.split('=')
            params[key] = unquote(value.replace('+', ' '))
        return params


server = GradeServer('127.0.0.1', 6000)
server.start()
```

   Запуск:
```bash
python3 server.py
```

2. Обновление данных:
   
   Необходимо послать POST запрос по адресу ```localhost:5000```
   
   Запрос должен содержать данные:

   - discipline : string (required)
   - grade : int (required)

3. Просмотр данных

    a. GET запрос любым способом

    b. Просмотреть в браузере страницу ```localhost:5000```
