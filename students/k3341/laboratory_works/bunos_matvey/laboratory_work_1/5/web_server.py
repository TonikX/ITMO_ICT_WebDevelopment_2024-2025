import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

grouped_grades = {}


def handle_client(conn, addr):
    request = conn.recv(1024).decode()
    headers = request.split('\r\n')
    method, path, protocol = headers[0].split(' ')
    print(f"Received {method} request from {addr}")

    if method == 'GET':
        response_body = generate_html()
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(response_body)}

{response_body}"""
        conn.sendall(response.encode())

    elif method == 'POST':
        content_length = 0
        for header in headers:
            if header.startswith('Content-Length:'):
                content_length = int(header.split(':')[1].strip())
                break
        body = request.split('\r\n\r\n')[1]
        if len(body) < content_length:
            body += conn.recv(content_length - len(body)).decode()

        params = parse_post_data(body)
        discipline = params.get('discipline', '')
        grade = params.get('grade', '')
        grouped_grades[discipline] = grouped_grades.get(discipline, []) + [grade]

        response_body = 'Data received'
        response = f"""HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: {len(response_body)}

{response_body}"""
        conn.sendall(response.encode())

    else:
        response_body = 'Method not allowed'
        response = f"""HTTP/1.1 405 Method Not Allowed
Content-Type: text/plain
Content-Length: {len(response_body)}

{response_body}"""
        conn.sendall(response.encode())

    conn.close()


def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Grades</title>
</head>
<body>
    <h1>Grades</h1>
    <table border="1">
        <tr><th>Discipline</th><th>Grade</th></tr>"""
    for discipline in grouped_grades:
        html += f"<tr><td>{discipline}</td><td>{','.join(grouped_grades[discipline])}</td></tr>"
    html += """
    </table>
</body>
</html>"""
    return html


def parse_post_data(data):
    params = {}
    pairs = data.split('&')
    for pair in pairs:
        key, value = pair.split('=')
        params[key] = value.replace('+', ' ')
    return params


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Web server started on port", PORT)
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
