# Задание 5

### Описание задачи

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Задание:**

_Сервер должен:_

* Принять и записать информацию о дисциплине и оценке по дисциплине.
* Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.


### Реализация

##### Стэк
* Python: 3.10
* Библиотека: socket

**Серверная часть:**
```
import socket

class MyHTTPServer:
    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = name
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._marks: dict = {}

    def serve_forever(self):
        try:
            self._server.bind((self._host, self._port))
            self._server.listen()
            while True:
                conn, address = self._server.accept()
                self.serve_client(conn)
        finally:
            self._server.close()

    def serve_client(self, conn):
        try:
            data = conn.recv(1024).decode()
            print('get a request')
            reqst = self.parse_request(data)
            print(f'request {reqst}')
            page = self.handle_request(reqst)
            self.send_response(reqst, page, conn)
        finally:
            conn.close()

    def parse_request(self, data):
        reqst = data.split("\r\n")
        method, target, version = reqst[0].split(" ")
        headers = self.parse_headers(str(reqst[1:]))
        body = data.split('\r\n\r\n')[1]
        return {'method': method, 'target': target, 'version': version, 'headers': headers, 'data': body}

    def parse_headers(self, reqst):
        end_of_headers = reqst.find('\r\n\r\n')
        headers = reqst[:end_of_headers].split('\r\n')
        headers_dict = {}
        for h in headers:
            k, v = h.split(':', 1)
            headers_dict[k] = v
        return headers_dict

    def handle_request(self, reqst):
        if reqst['method'] == 'POST':
            subject_list = reqst['data'].split('&')
            # Validate the data
            if len(subject_list) >= 2:
                new_subject = subject_list[0].split('=')[1]
                new_mark = subject_list[1].split('=')[1]
                self._marks[new_subject] = new_mark
            else:
                return '<h1>BadRequest: Invalid request data.</h1>'  # Handle error

        return self.generate_page()

    def send_response(self, reqst, page, conn) :
        conn.sendall(f"HTTP/1.1 200 OK\r\n{reqst['headers']}\r\n\r\n{page}".encode())

    def generate_page(self) :
        print('generate html page')
        html = '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><title>Оценки</title></head><body>'
        html += '<form method="POST">'
        html += '<label for="subject" lang="ru">Предмет:</label>'
        html += '<input type="text" id="subject" name="subject">'
        html += '<label for="mark" lang="ru">Оценка:</label>'
        html += '<input type="text" id="mark" name="mark">'
        html += '<input type="submit" value="Добавить оценку">'
        html += '</form>'
        html += "<table><thead><tr><th lang='ru'>Название предмета</th><th lang='ru'>Оценка</th></tr></thead><tbody>"
        for subject, mark in self._marks.items() :
            html += f"<tr><td>{subject}</td><td>{mark}</td></tr>"
        html += "</tbody></table>"
        html += '</body></html>'
        return html


if __name__ == "__main__":
    server = MyHTTPServer("127.0.0.1", 8000, "MarksServer")
    server.serve_forever()
```