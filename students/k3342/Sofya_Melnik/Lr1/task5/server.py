from socket import socket, AF_INET, SOCK_STREAM
from collections import defaultdict


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.scores = defaultdict(list)

    def serve(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(7)
        print(f"http://{self.host}:{self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            self.serve_client(client_socket)

    def serve_client(self, client_socket):
        request_data = client_socket.recv(1024).decode('utf-8')
        method, url, version = self.parse_request(request_data)

        if method == 'GET':
            response = self.handle_get_request(url)
        elif method == 'POST':
            response = self.handle_post_request(url, request_data)

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def parse_request(self, request_data):
        lines = request_data.split('\n')
        method, url, version = lines[0].split()
        return method, url, version

    def parse_headers(self, request_data):
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
            return self.subject_html()
        else:
            return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

    def handle_post_request(self, url, scores):
        if url == '/add_score':
            parameters = scores.split('\n')[-1]
            subject, score = self.post_parse(parameters)
            self.scores[subject].append(score)
            return self.subject_html()
        else:
            return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nNot Found"

    def post_parse(self, parameters):
        parameters = parameters.split('&')
        subject = None
        score = None
        for param in parameters:
            key, value = param.split('=')
            if key == 'subject':
                subject = value
            elif key == 'score':
                score = value

        return subject, score

    def subject_html(self):
        html = """\
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Scores</title>
            <style>
                table {
                    border-collapse: collapse;
                    margin: auto;
                    width: 80%;
                }
                th, td {
                    border: 5px solid red;
                    text-align: center;
                    padding: 10px;
                }
                th {
                    background-color: #f8c8dc;
                }
            </style>            
        </head>
        <body>
            <h1 style="text-align: center;">Scores</h1>
            <table style="border: solid pink;">
                <tr>
                    <th>Subject</th>
                    <th>Score</th>
                    <th>Average score</th>
                </tr>
        """
        for subject, scores in self.scores.items():
            scores_values = [float(score) for score in scores]
            if scores_values:
                average_score = sum(scores_values) / len(scores_values)
            else:
                average_score = 0

            html += f"<tr><td>{subject}</td><td>{', '.join(scores)}</td><td>{average_score:.2f}</td></tr>"

        html += """\
            </table>
            <style>
                form {
                    width: 300px;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: white;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
            </style>
            <h2>Add grades</h2>
            <form method="post" action="/add_score">
                <input type="text" id="subject" name="subject", placeholder="Subject"><br>
                <input type="text" id="grade" name="score", placeholder="Score"><br>
                <input type="submit" value="Add">
            </form>
        </body>
        </html>
        """
        return f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n{html}"


if __name__ == '__main__':
    host = 'localhost'
    port = 44444
    serv = MyHTTPServer(host, port)
    try:
        serv.serve()
    except KeyboardInterrupt:
        pass