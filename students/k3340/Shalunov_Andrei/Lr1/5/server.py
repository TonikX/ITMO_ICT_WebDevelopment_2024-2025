import socket
from threading import Thread

grades_list = []


def handle_client(client_sock):
    request = client_sock.recv(1024).decode()
    method, body, content_length = parse_request(request)
    print(f"Новый {method} запрос")

    if method == 'GET':
        response_body = generate_html()
        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                + response_body
        )
        client_sock.sendall(http_response.encode())

    elif method == 'POST':
        data = body[:content_length]
        pairs = data.split('&')
        post_grades = {}

        for pair in pairs:
            key, value = pair.split('=')
            if key.startswith('subject'):
                subject_key = key
                subject_value = value
                post_grades[subject_key] = {'subject': subject_value, 'grade': None}
            if key.startswith('grade'):
                grade_key = key.replace('grade', 'subject')
                grade_value = value
                if grade_key in post_grades:
                    post_grades[grade_key]['grade'] = grade_value

        for key, value in post_grades.items():
            if value.get('subject') and value.get('grade'):
                subject_found = False
                for item in grades_list:
                    if item['subject'] == value['subject']:
                        item['grades'].append(value['grade'])
                        subject_found = True
                        break

                if not subject_found:
                    grades_list.append({'subject': value['subject'], 'grades': [value['grade']]})


        response = """HTTP/1.1 200 OK
        Content-Type: text/plain

        Data successfully saved."""
        client_sock.sendall(response.encode())

    client_sock.close()


def parse_request(request):
    parts = request.split('\r\n\r\n')
    headers = parts[0]
    body = parts[1] if len(parts) > 1 else ''
    method, path, version = headers.split('\r\n')[0].split(' ')
    content_length = 0
    content_length_header = [head for head in headers.split('\r\n') if "Content-Length" in head]
    if content_length_header:
        content_length = int(content_length_header[0].split(': ')[1])

    return method, body, content_length


def generate_html():
    sorted_grades = sorted(grades_list, key=lambda x: x['subject'])
    html_text = """
    <html>
    <head><title>My grades</title></head>
    <body>
        <h2>Shalunov Andrei marks</h2>
        <table border="3">
            <tr>
                <th>Subject</th>
                <th>Grade</th>
            </tr>"""
    for item in sorted_grades:
        subject = item["subject"]
        grades = item["grades"]
        html_text += f"""
        <tr>
            <td>{subject}</td>
            <td>{", ".join(grades)}</td>
        """

    html_text += """
        </table>
    </body>
    </html>"""

    return html_text


HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

while True:
    connection, _ = sock.accept()
    thread = Thread(target=handle_client, args=(connection,))
    thread.start()
