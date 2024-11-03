import socket
from urllib.parse import parse_qs
from html import escape

# Структура для хранения оценок по предметам
grades = {}

# Функция для генерации HTML-страницы с таблицей оценок
def generate_html():
    html = "<html><head><title>Journal of Grades</title></head><body>"
    html += "<h1>Journal of Grades</h1>"
    html += "<table border='1'><tr><th>Subject</th><th>Grades</th></tr>"

    for subject, scores in grades.items():
        html += f"<tr><td>{escape(subject)}</td><td>{', '.join(map(str, scores))}</td></tr>"

    html += "</table>"
    html += "</body></html>"
    return html

# Основная функция обработки запросов
def handle_request(request):
    if not request.strip():  # Проверка, что запрос не пустой
        return "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nEmpty request received."

    headers, _, body = request.partition("\r\n\r\n")
    lines = headers.splitlines()

    if not lines:
        return "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid request format."

    request_line = lines[0]
    method, path, _ = request_line.split()

    if method == "GET" and path == "/grades":
        response_body = generate_html()
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response_body
        return response

    elif method == "POST" and path == "/add_grade":
        params = parse_qs(body)
        subject = params.get("subject", [""])[0]
        grade = params.get("grade", [""])[0]

        if subject and grade:
            grades.setdefault(subject, []).append(grade)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nGrade added successfully."
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMissing subject or grade."
        return response

    else:
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPage not found."
        return response

# Создание и запуск сервера
def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 8080))
        server_socket.listen(1)
        print("Server started on http://localhost:8080")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode("utf-8")
                response = handle_request(request)
                client_socket.sendall(response.encode("utf-8"))

# Запуск сервера
run_server()
