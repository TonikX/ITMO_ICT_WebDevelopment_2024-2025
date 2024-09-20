import socket
from colorama import Fore, init
init()

class HTTPServer:
    def __init__(self, host, port, name) -> None:
        self.host = host
        self.port = port
        self.name = name
        self.client = None
        self.working_dir = 'students/k3341/laboratory_works/Sergeev_Victor/lr1/task5/'
        self.db_path = self.working_dir + 'db.txt'
        self.methods = ('GET', 'POST', 'HEAD', 'DELETE', 'PUT', 'PATCH', 'OPTIONS', 'TRACE')

    def serve_forever(self):
        print(f'{Fore.YELLOW}Running a server - 127.0.0.1{Fore.RESET}')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()

            while True:
                self.client, _ = self.server.accept()
                print(f'{Fore.GREEN}Client connected{Fore.RESET}')
                try:
                    self.serve_client()
                except Exception as e:
                    print('Client serving failed:', e)
                finally:
                    pass
        finally:
            self.server.close()

    def serve_client(self):
        try:
            request = self.client.recv(1024).decode()
            print(f'{Fore.YELLOW}Server received:\n{Fore.WHITE}{request}{Fore.RESET}')
            self.handle_request(request)
        except ConnectionResetError:
            print(f'{Fore.GREEN}Lost client connection{Fore.RESET}')
            self.client = None
        except Exception as e:
            print('Internal error', e)

        if self.client:
            self.client.close()
            print(f'{Fore.GREEN}Client successfully disconnected{Fore.RESET}')
            self.client = None

    def handle_request(self, request):
        starting_line, headers = self.parse_request(request)
        print(f'{Fore.YELLOW}Request Parced{Fore.RESET}')
        code = starting_line['code']
        method = starting_line['method']
        version = starting_line['HTTPversion']

        if code == 400:  # 400 Bad Request
            content = self.get_http_code_page(400, version)
            self.send_responce(code, content)
            return
        if headers.get('host', '') != f'{self.host}:{self.port}':  # 400 Bad Request
            content = self.get_http_code_page(400, version)
            self.send_responce(400, content)
            return

        url = starting_line['url']
        if url == '/subjects':
            if method == 'GET':  # 200 OK
                template = open(self.working_dir + 'index.html').read()
                table = self.db_table_to_html()
                page = template.format(self.name, table)
                content = {'code_message': 'OK', 'HTTPversion': version, 'body': page}
                self.send_responce(200, content)
                return
            elif method == 'POST':  # 201 Created
                payload = headers['body']
                self.update_db(payload)
                content = self.get_http_code_page(201, version)
                self.send_responce(201, content)
                return
            else:  # 405 Method Not Allowed 
                content = self.get_http_code_page(405, version)
                self.send_responce(405, content)
                return
        else:  # 404 Not Found
            content = self.get_http_code_page(404, version)
            self.send_responce(404, content)
            return

    def parse_request(self, request):
        starting_line = self.parse_starting_ling(request)
        code = starting_line['code']
        if code // 100 != 2:
            return (starting_line, None)
        headers = self.parse_headers(request, starting_line['method'])
        return (starting_line, headers)

    def parse_starting_ling(self, request):
        code = 200
        line = request.split('\r\n')[0].split(' ')
        if len(line) > 3:
            code = 400
        try:
            method = line[0].upper()
            path = line[1]
            version = line[2]

            if method not in self.methods:
                code = 400
        except IndexError:
            code = 400

        if code == 400:
            path = ''
        
        if '?' in path:
            params = {}
            url, get_params = path.split('?')
            pairs = get_params.split('&')
            for pair in pairs:
                try:
                    k, v = pair.split('=')
                    params[k] = v
                except ValueError:
                    pass
        else:
            url = path
            params = {}
        
        if code == 400:
            return {'code': 400, 'method': None, 'url': None, 'HTTPversion': None, 'params': params}
        elif code == 200:
            return {'code': 200, 'method': method, 'url': url, 'HTTPversion': version, 'params': params}

    def parse_headers(self, request, method):
        header_lines = request.split('\r\n')[1:]
        headers = {}

        for line in header_lines:
            if line == '':  # means end of request or body is next
                break
            try:
                k, v = line.split(': ')
                headers[k.lower()] = v
            except ValueError:
                pass
        
        if method != 'POST':
            headers['body'] = ''
        else:
            if headers.get('content-type', '') == 'application/x-www-form-urlencoded':
                try:
                    length = int(headers['content-length'])
                    content = header_lines[-1]
                    headers['body'] = content[:length]
                except (KeyError, ValueError):
                    headers['body'] = ''
        return headers

    def get_http_code_page(self, code, version):
        HTTPcodes = {400: 'Bad Request', 404: 'Not Found', 405: 'Method Not Allowed', 201: 'Created'}
        message = HTTPcodes[code]
        template = open(self.working_dir + 'HTTPcodeTemplate.html').read()
        page = template.format(code, message)
        content = {'code_message': message, 'HTTPversion': version, 'body': page}
        return content

    def send_responce(self, code, content):
        message = content['code_message']
        version = content['HTTPversion']
        body = content['body']
        responce =  f'{version} {code} {message}\r\n' + \
                    'Connection: close\r\n'
        if len(body) != 0:
            responce += 'Content-Type: text/html; charset=utf-8;\r\n' + \
                        f'Content-Length: {len(body)}\r\n\r\n' + body
        self.client.sendall(responce.encode())
        print(f'{Fore.YELLOW}Server sent:\n{Fore.WHITE}{responce}{Fore.RESET}')

    def read_db(self):
        db = {}
        with open(self.db_path) as db_file:
            while ((line := db_file.readline()) != ''):
                subject, grades = line.replace('\n', '').split(':')
                db[subject] = grades.split()
        return db

    def update_db(self, payload):
        db = self.read_db()
        pairs = payload.split('&')
        for pair in pairs:
            try:
                k, v = pair.split('=')
                int(v)
                if db.get(k, None):
                    db[k].append(v)
                else:
                    db[k] = [v]
            except ValueError:
                pass
        with open(self.db_path, 'w') as db_file:
            for subject in list(db.keys()):
                db_file.write(f'{subject}:{" ".join(db[subject])}\n')
        
    def db_table_to_html(self):
        db = self.read_db()
        table = '  <table>\n'
        row_format = '    <tr>\n      <td>{0}</td>\n      <td>{1}</td>\n    </tr>\n'
        for subject in list(db.keys()):
            row = row_format.format(subject, ' '.join(db[subject]))
            table += row
        table += '  </table>\n'
        return table

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 16000
    name = 'ISU ITMO'
    server = HTTPServer(HOST, PORT, name)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass