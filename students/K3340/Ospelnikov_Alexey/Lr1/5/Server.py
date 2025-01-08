import socket
import json
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs
from datetime import datetime

max_headers = 100


class HTTPRequest:
    def __init__(self, method, url, version, headers, r_body):
        self.method = method
        self.url = url
        self.version = version
        self.headers = headers
        self.body = r_body

    @property
    def parsed_url(self):
        return urlparse(self.url)

    @property
    def query(self):
        return parse_qs(self.parsed_url.query)


class HTTPResponse:
    def __init__(self, code, status, version, headers=None, body=None):
        self.code = code
        self.status = status
        self.version = version
        self.headers = headers
        self.body = body

    def compile(self):
        resp = f"{self.version} {self.code} {self.status}\n"
        if self.headers:
            for header, value in self.headers.items():
                resp += f"{header}: {value}\n"
        if self.body:
            resp += f"\n{self.body}"
        return resp


def compile_html(req, filename, json_file):
    soup = bs(open(filename, 'r+'), "html.parser")
    caption = soup.find('h2', {'id': 'subj_name'})
    mark_list = soup.find('ul', {'id': 'marks'})
    try:
        subj = req.query['subject'][0]
        caption.string = f"Оценки по предмету: {subj}"
        with open(json_file, 'r') as grades_file:
            subjects = json.load(grades_file)
            marks = subjects[subj]
        for mark in marks:
            mark_li = soup.new_tag('li')
            mark_li.string = mark
            mark_list.append(mark_li)
        return soup.prettify('utf-8').decode()
    except KeyError:
        raise Exception("Wrong request parameters")


class HTTPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.name = "MyHTTPServer"
        self.http_v = "HTTP/1.1"

    def serve_forever(self):
        serv_sock = socket.socket()
        serv_sock.bind((self.ip, self.port))
        serv_sock.listen()
        try:
            while True:
                conn_socket, addr = serv_sock.accept()
                self.serve_client(conn_socket)
        finally:
            serv_sock.close()

    def serve_client(self, connection):
        req = self.parse_request(connection)
        if req:
            resp = self.handle_request(req).compile()
            resp_encoded = resp.encode()
            connection.sendall(resp_encoded)
        connection.close()

    def parse_request(self, connection):
        with connection.makefile('rb') as req_file:
            raw_first_line = req_file.readline()
            first_line = str(raw_first_line, 'utf-8')
            method, url, version = first_line.split()
            headers = self.parse_headers(req_file)
            return HTTPRequest(method, url, version, headers, req_file)

    def parse_headers(self, rfile):
        headers = dict()
        while len(headers) <= max_headers:
            r_line = rfile.readline().decode('utf-8')
            if r_line == '\n' or r_line == '' or r_line == '\r\n':
                return headers
            header, value = tuple(r_line.split())
            headers[header] = value
        raise Exception('too many headers')

    def handle_request(self, req):
        if req.parsed_url.path == "/grades":
            if req.method == "GET":
                html = compile_html(req, "html/index.html",
                                    "json/grades.json")
                resp_headers = {
                    "Server": self.name,
                    "Date": str(datetime.now()),
                    "Content-Length": len(html),
                    "Content-Type": "text/html; charset=utf-8"
                }
                return HTTPResponse(200, "OK", self.http_v, resp_headers, html)
            elif req.method == "POST":
                with open("json/grades.json", "r+") as grades_file:
                    subjects = json.load(grades_file)
                    try:
                        subjects[req.query["subject"][0]].append(req.query["mark"][0])
                    except KeyError:
                        raise Exception("Wrong request parameters")
                    grades_file.seek(0)
                    json.dump(subjects, grades_file)
                    grades_file.truncate()
                return HTTPResponse(204, "Created", self.http_v)
        else:
            return HTTPResponse(400, "Bad Request", self.http_v)


if __name__ == '__main__':
    host = '127.0.0.1'
    _port = 8080
    serv = HTTPServer(host, _port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass