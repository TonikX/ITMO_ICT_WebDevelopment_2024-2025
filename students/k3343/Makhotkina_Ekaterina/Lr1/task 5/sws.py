import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
grouped_grades = {}


def handle_client(connection, address):
    request = connection.recv(1024).decode()
    parts = request.split(' ')
    if len(parts) >= 3:
        method, path, protocol = parts[0:3]
        print(f"Получен {method} запрос от {address}")
        if method == 'GET':
            send_response(connection, '200 OK', 'Content-Type: text/html', provide_with_html())
        elif method == 'POST':
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            body = request.split('\r\n\r\n', 1)[1]
            while len(body.encode('utf-8')) < content_length:
                body += connection.recv(1024).decode()
            params = parse_post_data(body)
            discipline, grade = params.get('discipline', ''), params.get('grade', '')
            grouped_grades[discipline] = grouped_grades.get(discipline, []) + [grade]
            send_response(connection, '200 OK', 'Content-Type: text/plain', 'Принято!')
        else:
            send_response(connection, '405 Method is Not Allowed', 'Content-Type: text/plain',
                          'К сожалению, такого метода нет в листе разрешенных, попробуйте еще раз(((((')
    else:
        send_response(connection, '400 Bad Request', 'Content-Type: text/plain', 'Ошибка')
    connection.close()


def send_response(connection, status, content_type, body):
    response = f"""HTTP/1.1 {status}
{content_type}
Content-Length: {len(body)}

{body}"""
    connection.sendall(response.encode())


def parse_post_data(data):
    return {key: value.replace('+', ' ') for key, value in [pair.split('=') for pair in data.split('&')]}


def provide_with_html():
    rows = ''.join([f"<tr><td>{discipline}</td><td>{','.join(grades)}</td></tr>" for discipline, grades in grouped_grades.items()])
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Grades</title>
</head>
<body>
    <h1>Grades</h1>
    <table border="1">
        <tr><th>Discipline</th><th>Grade</th></tr>
        {rows}
    </table>
</body>
</html>"""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Сервер на порте", PORT)
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
