import socket
from urllib.parse import unquote_plus

grades = {}


def generate_html():
    html = """
    <html>
        <head><meta charset='UTF-8'><title>Grades by Subject</title></head>
        <body>
            <h1>Grades by Subject</h1>
            <table border="1">
                <tr>
                    <th>Subject</th>
                    <th>Grades</th>
                </tr>
    """
    for subject, grade_list in grades.items():
        grades_str = ", ".join(grade_list)
        html += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"

    html += """
            </table>
            <h2>Add a new grade</h2>
            <form method="POST">
                Subject: <input type="text" name="subject"><br>
                Grade: <input type="text" name="grade"><br>
                <input type="submit" value="Add">
            </form>
        </body>
    </html>
    """
    return html


def parse_post_data(data):
    post_data = {}
    params = data.split('&')
    for param in params:
        key, value = param.split('=')
        post_data[key] = unquote_plus(value)
    return post_data

def handle_request(request):
    headers, _, body = request.partition('\r\n\r\n')
    lines = headers.splitlines()
    request_line = lines[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

    elif method == 'POST':
        post_data = parse_post_data(body)
        subject = post_data.get('subject', '')
        grade = post_data.get('grade', '')
        if subject in grades:
            grades[subject].append(grade)
        else:
            grades[subject] = [grade]
        response_body = generate_html()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
        return response

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Сервер запущен на порту 8080...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Получен запрос от {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        if request:
            response = handle_request(request)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()


if __name__ == "__main__":
    run_server()