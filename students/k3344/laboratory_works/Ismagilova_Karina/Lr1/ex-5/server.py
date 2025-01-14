import socket
from collections import defaultdict
import urllib.parse

class MyHTTPServer:
    df = defaultdict(list)

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        print("Сервер запущен")
        try:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, connection):
        try:
            req = self.parse_request(connection)
            resp = self.handle_request(req)
            self.send_response(connection, resp)
        except ConnectionResetError:
            connection = None
        except Exception as e:
            self.send_error(connection, e)
        finally:
            if connection:
                connection.close()

    def parse_request(self, connection):
        reader = connection.makefile('r')
        request_line = reader.readline().strip()
        method, url, version = request_line.split()
        headers = self.parse_headers(reader)

        body = None
        if method == 'POST':
            content_length = int(headers.get('Content-Length', 0))
            body = reader.read(content_length)

        return {
            "method": method,
            "path": url,
            "headers": headers,
            "body": body
        }

    def parse_headers(self, reader):
        headers = {}
        while True:
            line = reader.readline().strip()
            if not line:
                break
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    def handle_request(self, req):
        if req["method"] == "GET" and req["path"] == "/":
            return self.serve_index_html()
        elif req["method"] == "POST" and req["path"] == "/":
            return self.handle_post(req)
        else:
            return self.http_response(404, "Not Found", "Страница не найдена")

    def serve_index_html(self):
        grades_html = self.generate_grades_table()
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                # Вставляем таблицу с оценками в HTML
                content = content.replace("{{ grades }}", grades_html)
                return self.http_response(200, "OK", content)
        except FileNotFoundError:
            return self.http_response(404, "Not Found", "Файл index.html не найден")

    def generate_grades_table(self):
        grades_html = "<table border='1'><tr><th>Дисциплина</th><th>Оценки</th></tr>"
        for subject, grades in self.df.items():
            grades_html += f"<tr><td>{subject}</td><td>{', '.join(grades)}</td></tr>"
        grades_html += "</table>"
        return grades_html

    def handle_post(self, req):
        try:
            body = req["body"]
            params = self.parse_post_params(body)

            discipline = params.get("discipline")
            grade = params.get("grade")

            if discipline and grade:
                self.df[urllib.parse.unquote(discipline)].append(str(grade))
                print(f"Добавлено: {discipline} - {grade}")  # Вывод в терминал
                return self.http_response(200, "OK", self.serve_index_html())
            else:
                return self.http_response(400, "Bad Request", "Необходимо указать дисциплину и оценку")
        except Exception as e:
            return self.http_response(400, "Bad Request", f"Ошибка: {str(e)}")

    def parse_post_params(self, body):
        params = {}
        for pair in body.split("&"):
            key, value = pair.split("=")
            params[key] = urllib.parse.unquote(value)
        return params

    def send_response(self, connection, response):
        connection.sendall(response.encode('utf-8'))

    def send_error(self, connection, error):
        response = self.http_response(500, "Internal Server Error", str(error))
        self.send_response(connection, response)

    def http_response(self, status_code, reason, content=""):
        response_line = f"HTTP/1.1 {status_code} {reason}\r\n"
        headers = "Content-Type: text/html; charset=utf-8\r\n"
        headers += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
        headers += "\r\n"
        return response_line + headers + content

    def clear_data(self):
        self.df.clear()
        print("Данные очищены.")

if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    server = MyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Сервер остановлен")
        server.clear_data()
