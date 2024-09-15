import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

grades = []


def handler(sock):
    request = sock.recv(1024).decode()
    headers, body = parse_request(request)
    method = headers[0].split(' ')[0]

    print(f"New {method}")

    if method == 'GET':
        handle_get(sock)
    elif method == 'POST':
        handle_post(sock, body)

    sock.close()


def parse_request(request):
    parts = request.split('\r\n\r\n')
    headers = parts[0].split('\r\n')
    body = parts[1] if len(parts) > 1 else ''
    return headers, body


def handle_get(sock):
    response_body = generate_html()
    response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(response_body)}

{response_body}"""
    sock.sendall(response.encode())


def handle_post(sock, body):
    params = parse_post_data(body)
    discipline = params.get('discipline', '')
    grade = params.get('grade', '')

    if discipline and grade:
        grades.append({'discipline': discipline, 'grade': grade})

    response_body = 'Data received'
    response = f"""HTTP/1.1 200 OK
Content-Type: text/plain

{response_body}"""
    sock.sendall(response.encode())


def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Grades</title>
</head>
<body>
    <h1>LR1 Yurkin Alexander K3340</h1>
    <h1>Grades</h1>
    <table border="1">
        <tr><th>Discipline</th><th>Grade</th></tr>"""

    for entry in grades:
        html += f"<tr><td>{entry['discipline']}</td><td>{entry['grade']}</td></tr>"

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


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((HOST, PORT))

print("Server started!")

serv.listen()

while True:
    sock, _ = serv.accept()
    thread = threading.Thread(target=handler, args=(sock,))
    thread.start()
