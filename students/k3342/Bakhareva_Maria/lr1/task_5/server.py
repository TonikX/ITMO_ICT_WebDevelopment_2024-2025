import socket
from urllib.parse import parse_qs

# Список для хранения оценок
grades = []


def load_html_template():
    """Загружает HTML-шаблон из файла."""
    with open('index.html', 'r', encoding='utf-8') as file:
        return file.read()


def handle_client(conn):
    """Обрабатывает запросы клиента."""
    request = conn.recv(1024).decode()
    print(f"Запрос:\n{request}")

    # Разделяем запрос на строки
    lines = request.splitlines()
    request_line = lines[0].split()

    # Обработка GET-запроса
    if request_line[0] == 'GET':
        # Формируем HTML-страницу с оценками
        html_template = load_html_template()
        grades_list = "".join(f"<li>{discipline}: {grade}</li>" for discipline, grade in grades)
        response_html = html_template.replace('<ul id="grades-list"></ul>', f'<ul id="grades-list">{grades_list}</ul>')

        response = "HTTP/1.1 200 OK\n"
        response += "Content-Type: text/html; charset=utf-8\n"
        response += "Connection: close\n\n"
        response += response_html
        conn.sendall(response.encode())

    # Обработка POST-запроса
    elif request_line[0] == 'POST':
        # Получаем тело запроса
        body = lines[-1]
        print(f"Тело POST-запроса: {body}")  # Отладочная информация

        # Парсинг тела запроса
        params = parse_qs(body)
        subject = params.get('subject', [''])[0]
        grade = params.get('grade', [''])[0]

        print(f"Добавление - Предмет: '{subject}', Оценка: '{grade}'")  # Отладочная информация

        # Добавление оценки
        if subject and grade:  # Проверяем, что параметры не пустые
            grades.append((subject, grade))
            response = "HTTP/1.1 200 OK\n"
            response += "Content-Type: text/html; charset=utf-8\n"
            response += "Connection: close\n\n"
            response += "<html><body><h1>Оценка добавлена!</h1></body></html>"
            conn.sendall(response.encode())
        else:
            response = "HTTP/1.1 400 Bad Request\n"
            response += "Content-Type: text/html; charset=utf-8\n"
            response += "Connection: close\n\n"
            response += "<html><body><h1>Неверные параметры!</h1></body></html>"
            conn.sendall(response.encode())

    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)

    print("Сервер запущен. Ожидание подключений...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Подключен: {addr}")
            handle_client(conn)
    except KeyboardInterrupt:
        print("\nСервер остановлен вручную.")
    finally:
        server_socket.close()
        print("Сервер закрыт.")


# Запуск сервера
start_server()
