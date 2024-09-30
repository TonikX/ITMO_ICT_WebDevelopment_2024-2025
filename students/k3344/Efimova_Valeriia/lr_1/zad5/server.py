import socket
import urllib.parse


grades_data = {}

def generate_html():
    html_content = """
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .content {
                display: flex;
            }
            .form {
                flex: 1;
            }
            .table {
                flex: 1;
                margin-left: 20px;
                border: 1px solid black;
                padding: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h1>Оценки по дисциплинам</h1>
        <div class="content">
            <div class="form">
                <form method='POST' action='/'>
                    <label>Дисциплина:</label> <input type='text' name='discipline' required><br><br>
                    <label>Оценка:</label> <input type='text' name='grade' required><br><br>
                    <input type='submit' value='Отправить оценку'><br><br>
                </form>
            </div>
            <div class="table">
                <h2>Список оценок</h2>
                <table>
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценка</th>
                    </tr>
    """
    
    for discipline, grade in grades_data.items():
        html_content += f"<tr><td>{discipline}</td><td>{grade}</td></tr>"
    
    html_content += """
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def handle_post_request(body):
    post_data = urllib.parse.parse_qs(body)
    discipline = post_data.get('discipline', [None])[0]
    grade = post_data.get('grade', [None])[0]

    print(f"POST данные: дисциплина = {discipline}, оценка = {grade}")

    if discipline and grade:
        grades_data[discipline] = grade
        print(f"Сохранено: {discipline} -> {grade}")

def handle_client_connection(client_socket):
    request_data = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        request_data += data
        if b'\r\n\r\n' in request_data:
            break

    request_text = request_data.decode('utf-8')
    print(f"Получен запрос:\n{request_text}\n")

    if '\r\n\r\n' in request_text:
        headers_part, body = request_text.split('\r\n\r\n', 1)
    else:
        headers_part = request_text
        body = ''

    request_lines = headers_part.split('\r\n')
    request_line = request_lines[0]
    headers = {}
    for header_line in request_lines[1:]:
        if ': ' in header_line:
            key, value = header_line.split(': ', 1)
            headers[key] = value
    if request_line.startswith('POST'):
        content_length = int(headers.get('Content-Length', '0'))
        body_bytes = body.encode('utf-8')
        bytes_needed = content_length - len(body_bytes)
        while bytes_needed > 0:
            data = client_socket.recv(4096)
            body_bytes += data
            bytes_needed -= len(data)
        body = body_bytes.decode('utf-8')
        print(f"Тело POST-запроса: {body}")
        handle_post_request(body)

    response_body = generate_html()
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{response_body}"
    )

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8081))
    server_socket.listen(5)
    print("Сервер запущен на порту 8081...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")
        handle_client_connection(client_socket)

start_server()   