import http.client
import socket
import sys
from datetime import datetime
from urllib.parse import unquote
import threading
import typing as tp

HOST = "localhost"
PORT = 8080


class Logger:
    def __init__(self, service: tp.Union[object, str] = None):
        self.__red = "\033[31m"
        self.__yellow = "\033[33m"
        self.__green = "\033[32m"
        self.__white = "\033[37m"
        self.__reset = "\033[0m"
        if service is None:
            print("Логгер инициализирован без имени.")
        if isinstance(service, object) and service is not None:
            self.__service_name = service.__class__.__name__
        elif isinstance(service, str):
            self.__service_name = service
        else:
            self.__service_name = "UnnamedService"

    def info(self, msg):
        print(f"[{self.__gettime()}] {self.__green}[INFO]{self.__reset} [{self.__service_name}]: {msg}")

    def warn(self, msg):
        print(f"[{self.__gettime()}] {self.__yellow}[WARN]{self.__reset} [{self.__service_name}]: {msg}")

    def error(self, msg):
        print(f"{self.__gettime()}] {self.__red}[ERROR]{self.__reset} [{self.__service_name}]: {msg}")

    def __gettime(self):
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


grades_data = {}


class MyHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def serve_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((self._host, self._port))
            server.listen()
            server.settimeout(1)
            log.info(f"Сервер запущен на адресе {self._host}:{self._port}")
            while True:
                try:
                    conn, _ = server.accept()
                    client_thread = threading.Thread(target=self.serve_client, args=(conn,), daemon=True)
                    client_thread.start()
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    log.error(f"Что-то пошло не так: {e}")
        except KeyboardInterrupt:
            log.warn("Обнаружен ввод Ctrl+C")
        finally:
            log.info("Сервер останавливается...")
            server.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp, status_code = self.handle_request(req)
            self.send_response(conn, resp)
            self.log_request(req, status_code, http.client.responses[status_code])
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
        if conn:
            conn.close()


    def parse_request(self, conn):
        rfile = conn.makefile('rb')

        request_line = rfile.readline().decode('iso-8859-1').strip()
        method, path, version = request_line.split()

        headers = self.parse_headers(rfile)

        content_length = int(headers.get('Content-Length', 0))
        body = rfile.read(content_length).decode('iso-8859-1') if content_length else None

        return {
            'method': method,
            'path': path,
            'version': version,
            'headers': headers,
            'body': body
        }

    def parse_headers(self, rfile):
        headers = {}
        while True:
            line = rfile.readline().decode('iso-8859-1').strip()
            if not line:
                break
            header_name, header_value = line.split(":", 1)
            headers[header_name.strip()] = header_value.strip()
        return headers

    def handle_request(self, req):
        if req['method'] == 'GET' and req['path'] == '/grades':
            return self.build_response(200, self.render_grades())
        elif req['method'] == 'POST' and req['path'] == '/submit':
            body = req['body']
            if body:
                params = dict(pair.split('=') for pair in body.split('&'))
                discipline = unquote(params.get('discipline', '')).strip()
                grade = unquote(params.get('grade', '')).strip()

                if discipline and grade:
                    grades_data[discipline] = grade
                    return self.build_response(200, self.render_submission_success())
            return self.build_response(400, "Invalid POST request")
        else:
            return self.build_response(404, "Not Found")

    def build_response(self, status_code, body):
        response_line = f"HTTP/1.1 {status_code} {http.client.responses[status_code]}\r\n"
        headers = "Content-Type: text/html; charset=utf-8\r\n"
        headers += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        headers += "Connection: close\r\n"
        headers += "\r\n"
        response = response_line + headers + body
        return response, status_code

    def send_response(self, conn, resp):
        conn.sendall(resp.encode('utf-8'))

    def send_error(self, conn, err):
        resp, _ = self.build_response(500, f"Error: {err}")
        self.send_response(conn, resp)
        conn.close()

    def render_submission_success(self):
        return """
        <html><head><meta charset="UTF-8"><title>Submission Success</title></head><body>
        <h2>Data submitted successfully!</h2>
        <button onclick="window.location.href='/grades'">Return to Grades</button>
        </body></html>
        """

    def render_grades(self):
        html = "<html><head><title>Зачётка</title></head><body>"
        html += "<h1>Зачётка</h1>"
        if grades_data:
            html += "<ul>"
            for discipline, grade in grades_data.items():
                html += f"<li>{discipline}: {grade}</li>"
            html += "</ul>"
        else:
            html += "В зачётке пусто. Почему бы это не исправить? ;)"
        html += "<h3>Добавить запись:</h3>"
        html += """
        <form method="POST" action="/submit">
            <label for="discipline">Дисциплина:</label>
            <input type="text" id="discipline" name="discipline"><br>
            <label for="grade">Оценка:</label>
            <input type="text" id="grade" name="grade"><br>
            <input type="submit" value="Сохранить">
        </form>
        """
        html += "</body></html>"
        return html

    def log_request(self, req, status_code, status_text):
        log_message = (f"Request: {req['method']} {req['path']} | "
                       f"Response: {status_code} {status_text}")
        log.info(log_message)


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 2 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    serv = MyHTTPServer(HOST, PORT)
    log = Logger(serv)
    serv.serve_forever()
