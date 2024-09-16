from email.parser import Parser
from email.message import Message
from io import BufferedReader

import socket
import sys
import traceback

class Request:

    def __init__(self, method: str, target: str, params: dict[str, str], version: str, headers: dict[str, any], body: dict[str, str]):
        self.Method = method
        self.Target = target
        self.Params = params
        self.Version = version
        self.Headers = headers
        self.Body = body

    Method: str
    Target: str
    Params: dict[str, str]
    Version: str
    Headers: dict[str, any]
    Body: dict[str, str]

class Response:

    def __init__(self, status: int, reason: str, headers: bytes = None, body: bytes = None):
        self.Status: int = status
        self.Reason: str = reason
        self.Headers: bytes = headers
        self.Body: bytes = body

class MyHTTPServer:
    
    _host: int
    _port: int
    _name: int
    _coding: str

    def __init__(self, host: int, port: int, name: str, coding: str):
        self._host = host
        self._port = port
        self._name = name
        self._coding = coding
    
    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений

        sock = socket.socket()
        sock.bind((self._host, self._port))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()
            self.serve_client(conn, addr)


    def serve_client(self, conn: socket.socket, addr: list[any]):
        # 2. Обработка клиентского подключения

        print(f"Установлено соединения с клиентом {addr[0]}:{addr[1]}")
        
        conn.settimeout(5)

        try:
            request = self.parse_request(conn)
            response = self.handle_request(request)
            self.send_response(conn, response)

        except ConnectionResetError:
            traceback.print_exc()
            conn = None

        except Exception:
            response = Response(400, "Bad Request")
            self.send_response(conn, response)
            traceback.print_exc()

        finally:
            if conn:
                conn.close()


    def parse_request(self, conn: socket.socket) -> Request:
        # 3. функция для обработки заголовка http+запроса. Python, сокет предоставляет возможность создать вокруг него некоторую обертку, которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос. Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента    (метод + url + версия протокола). URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        reqFile = conn.makefile("rb")
        
        reqLine = reqFile.readline(MAX_SIZE)
        if not reqLine.endswith("\r\n".encode(self._coding)):
            raise Exception('Header line is too long')

        method, url, version = reqLine.decode(self._coding).split(" ")
        method = method.strip()
        url = url.strip()
        version = version.strip()
        
        urlSplit = url.split("?")

        if len(urlSplit) == 1:
            target = urlSplit[0]
            paramsString = ""

        elif len(urlSplit) == 2:
            target, paramsString = url.split("?")

        else:
            raise Exception("Invalid url")

        params = self.parse_params_string(paramsString)
        headers = self.parse_headers(reqFile)

        body = dict()
        if headers.get("Content-Length"):
          body = self.parse_body(reqFile, int(headers.get("Content-Length")))

        reqFile.close()

        return Request(method, target, params, version, headers, body)

    def parse_params_string(self, paramsString: str) -> dict[str, any]:

        params = dict()

        if not paramsString:
            return params

        for pairs in paramsString.split("&"):
            key, value = pairs.split("=")
            value.replace("+", " ")
            params[key] = value

        return params


    def parse_headers(self, reqFile: BufferedReader) -> Message:
        # 4. Функция для обработки headers. Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        headers = []

        while True:
            header = reqFile.readline(MAX_SIZE)
            if not header.endswith("\r\n".encode(self._coding)):
              raise Exception('Header line is too long')
            
            headers.append(header)
            
            if header == b"\r\n":
                break
            
        headersMessage = Parser().parsestr(b''.join(headers).decode('iso-8859-1'))
        
        host = headersMessage.get("Host")
        if not host:
            raise Exception('Bad request')
        if host not in (self._name, f'{self._name}:{self._port}'):
            raise Exception('Not found')
        
        return headersMessage
        

    def parse_body(self, reqFile: BufferedReader, bodyLen: int) -> dict[str, any]:
        body = reqFile.read(bodyLen)

        return self.parse_params_string(body.decode(self._coding))
       

    def handle_request(self, request: Request) -> Response:
        # 5. Функция для обработки url в соответствии с нужным методом. В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос. GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.

        match request.Method:
            case "GET":
                templateHtmlFile = open("template-grades.html", "r", encoding=self._coding)
                templateHtml = templateHtmlFile.read()
                templateHtmlFile.close()

                discipline = request.Params.get("discipline")
                if discipline == None:
                    raise Exception("Invalid GET parameters")

                gradesFile = open("grades.txt", "r", encoding=self._coding)
                
                gradesAll = gradesFile.readlines()
                grades = ""
                for grade in gradesAll:
                    if discipline in grade:
                        grades += grade + "\n"

                gradesFile.close()

                templateHtml = templateHtml.replace("{{rows}}", grades)

                body = templateHtml.encode(self._coding)
                headers = f"Content-Length: {str(len(body))}\r\nHost: {self._name}\r\n".encode(self._coding)

                return Response(200, "ОК", headers, body)

            case "POST":
                discipline = request.Body.get("discipline")
                mark = request.Body.get("mark")

                if discipline == None or mark == None:
                    raise Exception("Invalid POST parameters")
                
                with open("grades.txt", "a", encoding=self._coding) as file:
                    file.write(f"<tr><td>{discipline}</td><td>{mark}</td></tr>\n")

                return Response(204, 'Created')


            case _:
                raise Exception("Unsupported method")

    

    def send_response(self, conn: socket.socket, response: Response):
        # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>. Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        resFile = conn.makefile("wb")
        resLine = f"HTTP/1.1 {response.Status} {response.Reason}\r\n"

        resFile.write(resLine.encode(self._coding))
        if response.Headers:
            resFile.write(response.Headers)
        resFile.write("\r\n".encode(self._coding))
        if response.Body:
            resFile.write(response.Body)

        resFile.flush()
        resFile.close()
    

if __name__ == '__main__':
    
    MAX_SIZE = 65535

    host = "localhost"
    port = 14905
    name = "lb1"
    coding = "utf-8"
    serv = MyHTTPServer(host, port, name, coding)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass