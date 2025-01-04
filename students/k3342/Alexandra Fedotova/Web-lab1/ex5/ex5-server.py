import socket
from urllib.parse import parse_qs

# Хранилище для оценок в виде словаря
current_grades = {}

def load_html():
    with open('index2.html', 'r', encoding='utf-8') as file:
        return file.read()

def create_html():
    html_template = load_html()

    # Формирование списка оценок
    if current_grades:
        grades_list = ""
        for discipline, di_grades in current_grades.items():
            grades_str = ', '.join(di_grades)
            grades_list += f"<li>{discipline}: {grades_str}</li>"
    else:
        grades_list = "<li>Журнал пуст</li>"

    # Замена на реальный список оценок
    html_content = html_template.replace('{{grades_list}}', grades_list)
    return html_content


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Сервер запущен на http://localhost:8080")

while True:
    client_socket, addr = server_socket.accept()
    request = client_socket.recv(4096).decode()  # Увеличиваем буфер для чтения

    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        # Формируем ответ для GET-запроса
        response_body = create_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    elif method == 'POST':
        # Проверяем, есть ли тело в запросе
        if '\r\n\r\n' in request:
            headers, body = request.split('\r\n\r\n', 1)
        else:
            headers, body = request, ''

        # Извлекаем длину
        content_length = 0
        for header in headers.splitlines():
            if 'Content-Length' in header:
                content_length = int(header.split(':')[1].strip())

        # Если тело неполное, ждем оставшиеся данные
        while len(body) < content_length:
            body += client_socket.recv(4096).decode()

        # Получение данных из POST-запроса
        data = parse_qs(body)

        # Записываем дисциплину и оценку
        subject = data.get('subject', [''])[0].strip()
        grade = data.get('grade', [''])[0].strip()

        if subject and grade:
            # Если дисциплина уже существует, добавляем новую оценку в список
            if subject in current_grades:
                current_grades[subject].append(grade)
            else:
                current_grades[subject] = [grade]

        response_body = create_html()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' + response_body

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\n'

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()