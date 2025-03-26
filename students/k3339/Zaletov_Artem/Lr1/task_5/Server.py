import socket
from urllib.parse import parse_qs

grades = {}


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Fail', e)
        finally:
            serv_sock.close()

    def serve_client(self, client):
        try:
            req = self.parse_request(client)
            resp = self.handle_request(req)
            self.send_response(client, resp)
        except ConnectionResetError:
            client = None

        if client:
            client.close()

    def parse_request_line(self, rfile):
        line = rfile.readline()
        line = line.decode('utf-8')
        return line.split()

    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)

        request = {'data': {}, 'method': method}

        if method == 'POST':
            content_length = 0
            headers = []
            while True:
                header_line = rfile.readline().decode('utf-8')
                if header_line == '\r\n':
                    break
                headers.append(header_line.strip())

                if header_line.lower().startswith('content-length'):
                    content_length = int(header_line.split(':')[1].strip())

            body = rfile.read(content_length).decode('utf-8')
            request['data'] = parse_qs(body)

        elif '?' in target:
            request['method'] = 'GET'
            values = target.split('?')[1].split('&')
            for value in values:
                a, b = value.split('=')
                request['data'][a] = b

        return request

    def handle_request(self, req):
        if req['method'] == 'POST':
            return self.handle_post(req)
        else:
            return self.handle_get()

    def handle_get(self):
        content_type = 'text/html; charset=utf-8'
        body = '''
        <html>
        <head>
            <style>
                body {
                    background-color: #f4f7f6;
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }

                .container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 600px;
                }

                h1 {
                    text-align: center;
                    color: #fa8e47;
                    font-size: 36px;
                    margin-bottom: 20px;
                }

                .form-group {
                    margin-bottom: 20px;
                }

                .form-group label {
                    font-size: 18px;
                    color: #555;
                    display: block;
                    margin-bottom: 5px;
                }

                .form-group input {
                    width: 100%;
                    padding: 12px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    transition: border-color 0.3s;
                }

                .form-group input:focus {
                    border-color: #fa8e47;
                    outline: none;
                }

                .form-group button {
                    width: 100%;
                    padding: 14px;
                    background-color: #fa8e47;
                    color: #fff;
                    font-size: 18px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .form-group button:hover {
                    background-color: #e07c3c;
                }

                table {
                    width: 100%;
                    margin-top: 30px;
                    border-collapse: collapse;
                }

                table th, table td {
                    padding: 12px;
                    text-align: center;
                    border: 1px solid #ddd;
                    font-size: 18px;
                }

                table th {
                    background-color: #fa8e47;
                    color: #fff;
                }

                table tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Добавить оценку</h1>
                <form method="post">
                    <div class="form-group">
                        <label for="discipline">Предмет</label>
                        <input type="text" id="discipline" name="discipline" required />
                    </div>
                    <div class="form-group">
                        <label for="grade">Оценка</label>
                        <input type="number" id="grade" name="grade" min="1" max="5" required />
                    </div>
                    <div class="form-group">
                        <button type="submit">Добавить</button>
                    </div>
                </form>

                <table>
                    <thead>
                        <tr>
                            <th>Дисциплина</th>
                            <th>Оценки</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        for subject in grades:
            body += f'<tr> <td>{subject}</td> <td>{", ".join(grades[subject])}</td> </tr>'
        body += '''
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        '''
        body = body.encode('utf-8')
        headers = [('Content-Type', content_type)]
        return Response(200, 'OK', headers, body)

    def handle_post(self, request):
        discipline = request['data']['discipline'][0]
        grade = request['data']['grade'][0]

        if discipline not in grades:
            grades[discipline] = []
        if 1 <= int(grade) <= 5:
            grades[discipline].append(grade)

        return self.handle_get()

    def send_response(self, conn, resp):
        rfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        rfile.write(status_line.encode('utf-8'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                rfile.write(header_line.encode('utf-8'))

        rfile.write(b'\r\n')

        if resp.body:
            rfile.write(resp.body)

        rfile.flush()
        rfile.close()


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


if __name__ == '__main__':
    serv = MyHTTPServer('127.0.0.1', 8080)
    serv.serve_forever()
