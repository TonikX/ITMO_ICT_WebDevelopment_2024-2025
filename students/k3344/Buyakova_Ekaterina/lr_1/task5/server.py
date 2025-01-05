import socket
import threading
import urllib.parse

# Параметры сервера
HOST = 'localhost'
PORT = 8080
grades = []


def handler(sock):
    try:
        request = sock.recv(1024).decode()
        if not request:
            return
        headers, body = parse_request(request)
        method = headers[0].split(' ')[0]

        print(f"New {method}")

        if method == 'GET':
            handle_get(sock)
        elif method == 'POST':
            handle_post(sock, body)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


def parse_request(request):
    # Разделяем заголовки и тело запроса
    parts = request.split('\r\n\r\n')
    headers = parts[0].split('\r\n')
    body = parts[1] if len(parts) > 1 else ''
    return headers, body


def handle_get(sock):
    response_body = generate_html()

    # Добавляем Content-Length, чтобы указать длину тела ответа
    response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(response_body)}

{response_body}"""

    sock.sendall(response.encode())


def handle_post(sock, body):
    params = parse_post_data(body)
    discipline = params.get('discipline', '')
    grade = params.get('grade', '')

    if discipline and grade:
        existing = next((item for item in grades if item['discipline'] == discipline), None)
        if existing:
            existing['grade'] += f", {grade}"
        else:
            grades.append({'discipline': discipline, 'grade': grade})

    # Перенаправляем на главную страницу после POST-запроса
    response = """HTTP/1.1 302 Found
Location: /
Content-Length: 0

"""
    sock.sendall(response.encode())


def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Grades</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f4f4f4;
        }
        form {
            margin: 20px 0;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 8px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #28a745;
            border: none;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <h1>Grades</h1>
    <table>
        <tr>
            <th>Discipline</th>
            <th>Grades</th>
        </tr>"""

    for entry in grades:
        html += f"<tr><td>{entry['discipline']}</td><td>{entry['grade']}</td></tr>"

    html += """
    </table>
    <form method="POST" action="/">
        <label for="discipline">Discipline:</label>
        <input type="text" id="discipline" name="discipline" required>
        <label for="grade">Grade:</label>
        <input type="text" id="grade" name="grade" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>"""
    return html


def parse_post_data(data):
    # Разбираем данные POST-запроса
    params = {}
    pairs = data.split('&')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            params[key] = urllib.parse.unquote(value)
    return params


# Настраиваем сервер
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((HOST, PORT))

print(f"Server starts on {HOST}:{PORT}")

serv.listen()

while True:
    sock, _ = serv.accept()
    thread = threading.Thread(target=handler, args=(sock,))
    thread.start()
