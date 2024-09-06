from socket import socket, AF_INET, SOCK_STREAM

from utils import CSV_handler, table_handler, generate_page

"""
Задание: сделать сервер, который может:
● Принять и записать информацию о дисциплине и оценке по дисциплине.
● Отдать информацию обо всех оценках по дисциплине в виде html-страницы.
"""


class MyHTTPServer:
    def __init__(self,
                 host_address,
                 host_port,
                 data_handler: table_handler = CSV_handler('static/data.csv'),
                 ):
        self._port = host_port
        self._host = host_address
        self._data_handler = data_handler

    def serve_forever(self):
        serv_sock = socket(
            AF_INET,
            SOCK_STREAM,
            proto=0)

        serv_sock.bind((self._host, self._port))
        serv_sock.listen(10)
        print(f"Сервер запущен на {self._host}:{self._port}")

        try:
            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, client_socket):
        response = client_socket.recv(1024).decode('utf-8')
        method, url, _ = self.parse_request(response)

        match method:
            case 'GET':
                response = self.handle_get_request(url)
            case 'POST':
                response = self.handle_post_request(url, response)
            case _:
                response = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    @staticmethod
    def parse_request(request_data):
        lines = request_data.split('\n')
        method, url, version = lines[0].split()
        return method, url, version

    @staticmethod
    def parse_headers(request_data):
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
            return generate_page(self._data_handler.get_html_table(),
                                 './static/index.html')
        else:
            return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n\
            <head><meta http-equiv=\"Refresh\" content=\"0; \
            URL=http://localhost:12345\" /></head>\n\n"

    def handle_post_request(self, url, response):
        parameters = response.split('\n')[-1]
        parsed_response = self.parse_post(parameters)

        if url == '/add_grade':
            if all(['subject', 'grade', 'name'].count(i) for i in parsed_response):
                self._data_handler.append(parsed_response.values())
                return "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\n\
            <head><meta http-equiv=\"Refresh\" content=\"0; \
            URL=http://localhost:12345\" /></head>"

        if url == '/filter_by':
            print(parsed_response)
            if 'key' in parsed_response and 'value' in parsed_response:
                filtered_content = self._data_handler.get_html_table(
                    content=self._data_handler.filter_by(parsed_response['key'], parsed_response['value'])
                )
                response = generate_page(filtered_content, './static/index.html')
                return response
            else:
                return "HTTP/1.1 400 Bad Request\nContent-Type: text/plain\n\nMissing filter parameters"
        else:
            return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

    @staticmethod
    def parse_post(post_request):
        post_request = post_request.split('&')
        request = {}
        for param in post_request:
            key, value = param.split('=')
            request[key] = value
        return request


if __name__ == '__main__':
    host = 'localhost'
    port = 12345
    serv = MyHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
