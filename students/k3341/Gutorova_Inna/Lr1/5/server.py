import socket

grades = {}


def generate_html():
    html = """
    <html>
        <head><title>Grades by Subject</title></head>
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
            <form method="POST" action="/">
                Subject: <input type="text" name="subject"><br>
                Grade: <input type="text" name="grade"><br>
                <input type="submit" value="Add">
            </form>
        </body>
    </html>
    """
    return html


def handle_get():
    response_body = generate_html()
    response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n" +
            response_body
    )
    return response


def handle_post(request):
    global grades

    body = request.split("\r\n\r\n")[1]
    params = body.split('&')

    subject = None
    grade = None

    for param in params:
        key, value = param.split('=')
        if key == 'subject':
            subject = value.replace('+', ' ')
        elif key == 'grade':
            grade = value.replace('+', ' ')

    if subject and grade:
        if subject in grades:
            grades[subject].append(grade)
        else:
            grades[subject] = [grade]

    return handle_get()


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(1)
    print("Server is running on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received request from {client_address}")

        request = client_socket.recv(1024).decode()
        if request.startswith("GET"):
            response = handle_get()
        elif request.startswith("POST"):
            response = handle_post(request)
        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    run_server()
