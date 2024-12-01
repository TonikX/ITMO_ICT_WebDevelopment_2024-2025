import socket
from urllib.parse import parse_qs


class MyHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.grades = {}

    def serve_forever(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Сервер запущен на {self._host}:{self._port}")

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Ошибка при обслуживании клиента:', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req, conn)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        request_data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            request_data += chunk
            if b'\r\n\r\n' in request_data:
                break

        request_text = request_data.decode('utf-8')
        print("Получен запрос:\n", request_text)
        lines = request_text.splitlines()
        method, path, _ = lines[0].split()

        if method not in ['GET', 'POST']:
            raise ValueError("Неподдерживаемый метод")

        return method, path, request_text, request_data

    def handle_request(self, req, conn):
        method, path, request_text, request_data = req

        if method == 'POST' and path == '/submit':
            headers = self.parse_headers(request_text)
            content_length = int(headers.get('Content-Length', 0))

            header_end = request_data.find(b'\r\n\r\n') + 4
            body_data = request_data[header_end:]

            remaining = content_length - len(body_data)
            while remaining > 0:
                chunk = conn.recv(remaining)
                if not chunk:
                    break
                body_data += chunk
                remaining -= len(chunk)

            body = body_data.decode('utf-8')
            post_data = parse_qs(body)

            discipline = post_data['discipline'][0]
            grade = post_data['grade'][0]

            if discipline in self.grades:
                self.grades[discipline].append(grade)
            else:
                self.grades[discipline] = [grade]

            response_body = self.generate_html()
            return self.create_response(response_body)

        elif method == 'GET' and path == '/':
            return self.create_response(self.generate_html())

        else:
            raise ValueError("Запрашиваемый путь не найден")

    def parse_headers(self, request_text):
        headers = {}
        lines = request_text.split('\r\n')
        for line in lines[1:]:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value
            elif line == '':
                break
        return headers

    def generate_html(self):
        html = "<html><body>"
        html += "<h1>Оценки по дисциплинам</h1>"
        html += '<form action="/submit" method="POST">'
        html += 'Дисциплина: <input type="text" name="discipline"><br>'
        html += 'Оценка: <input type="text" name="grade"><br>'
        html += '<input type="submit" value="Отправить">'
        html += '</form>'

        if self.grades:
            html += '<h2>Добавленные оценки:</h2><ul>'
            for discipline, grades in self.grades.items():
                grades_str = ', '.join(grades)
                html += f'<li>{discipline}: {grades_str}</li>'
            html += '</ul>'
        else:
            html += '<h2>Нет добавленных оценок.</h2>'

        html += '</body></html>'
        return html

    def create_response(self, body):
        """Создает HTTP-ответ с заданным содержимым."""
        response = (
            "HTTP/1.1 200 OK\r\n" 
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n" 
            "\r\n"
            f"{body}"
        )
        return response

    def send_response(self, conn, resp):
        conn.sendall(resp.encode('utf-8'))

    def send_error(self, conn, err):
        error_message = f'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\n{str(err)}'
        conn.sendall(error_message.encode('utf-8'))


if __name__ == '__main__':
    host = 'localhost'
    port = 8080

    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
