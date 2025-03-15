import socket
import threading
from urllib.parse import parse_qs

HOST = '127.0.0.1'
PORT = 8080
grades = {}


def handle_client(connection, address):
    try:
        request = connection.recv(1024).decode()
        if not request:
            return

        headers = request.splitlines()
        method = headers[0].split()[0]
        path = headers[0].split()[1]

        if method == 'POST' and path == '/add_grade':
            handle_post_request(headers, request)
            response = 'HTTP/1.1 302 Found\nLocation: /\n\n'
        elif method == 'GET' and path == '/':
            response = handle_get_request()
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\n\n'

        connection.sendall(response.encode())
    except Exception as e:
        print(f"Error handling request from {address}: {e}")
        connection.sendall('HTTP/1.1 500 Internal Server Error\n\n'.encode())
    finally:
        connection.close()


def handle_post_request(headers, request):
    content_length = int([h for h in headers if h.startswith('Content-Length:')][0].split(': ')[1])
    body = request.splitlines()[-1]
    data = parse_qs(body)
    discipline = data.get('subject', [''])[0]
    grade = data.get('grade', [''])[0]

    if discipline and grade:
        if discipline not in grades:
            grades[discipline] = []
        grades[discipline].append(grade)


def handle_get_request():
    rows = ''.join(
        [f"<tr><td>{discipline}</td><td>{','.join(grades)}</td></tr>" for discipline, grades in grades.items()])
    response_body = f"""<!DOCTYPE html>
<html>
<head>
    <title>Lisa Karnaukhova's grades</title>
</head>
<body>
    <h1>Grades</h1>
    <table border="0">
        <tr><th>Discipline</th><th>Grades</th></tr>
        {rows}
    </table>
    <form method="post" action="/add_grade">
        <input type="text" id="subject" name="subject" , placeholder="Subject"><br>
        <input type="number" id="grade" name="grade" , placeholder="Grade"><br>
        <input type="submit" value="Add">
    </form>
</body>
</html>"""

    return f'HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {len(response_body)}\n\n{response_body}'


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен http://{HOST}:{PORT}")
        while True:
            connection, address = s.accept()
            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()


if __name__ == "__main__":
    start_server()
