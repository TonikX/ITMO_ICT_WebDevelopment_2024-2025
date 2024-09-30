import socket
from urllib.parse import parse_qs

# Хранилище оценок: ключ — дисциплина, значение — список оценок
grades_db = {}

# Загрузка шаблона HTML из файла
def load_template():
    with open('index5.html', 'r', encoding='utf-8') as template_file:
        return template_file.read()

# Создание HTML с оценками, вставляя данные из хранилища
def generate_grades_page():
    html_template = load_template()

    # Создание списка оценок
    if grades_db:
        grades_items = ""
        for subject, grades in grades_db.items():
            grades_list = ', '.join(grades)
            grades_items += f"<li>{subject}: {grades_list}</li>"
    else:
        grades_items = "<li>Пока нет оценок</li>"

    # Вставляем оценки в HTML
    html_output = html_template.replace('{{grades_list}}', grades_items)
    return html_output


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9091))
server_socket.listen(5)

print("Веб-сервер работает на http://localhost:9091")

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(4096).decode('utf-8')  # Получаем запрос клиента

    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if method == 'GET':
        # Ответ на GET-запрос: отображение страницы с оценками
        response_content = generate_grades_page()
        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html; charset=utf-8\r\n\r\n'
            + response_content
        )

    elif method == 'POST':
        # Извлечение тела запроса из POST-запроса
        if '\r\n\r\n' in request:
            headers, body = request.split('\r\n\r\n', 1)
        else:
            headers, body = request, ''

        content_length = 0
        for header in headers.splitlines():
            if 'Content-Length' in header:
                content_length = int(header.split(':')[1].strip())

        while len(body) < content_length:
            body += client_socket.recv(4096).decode('utf-8')

        post_data = parse_qs(body)

        # Извлечение дисциплины и оценки из данных
        subject = post_data.get('subject', [''])[0].strip()
        grade = post_data.get('grade', [''])[0].strip()

        if subject and grade:
            # Если дисциплина уже есть, добавляем новую оценку
            if subject in grades_db:
                grades_db[subject].append(grade)
            else:
                grades_db[subject] = [grade]

        # Возвращаем обновлённую HTML-страницу
        response_content = generate_grades_page()
        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html; charset=utf-8\r\n\r\n'
            + response_content
        )

    else:
        response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
