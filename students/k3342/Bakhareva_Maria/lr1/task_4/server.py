import socket
import threading

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
        discipline, grade = body.split('=')
        grades.append((discipline.replace('%20', ' '), grade))

        response = "HTTP/1.1 200 OK\n"
        response += "Content-Type: text/html; charset=utf-8\n"
        response += "Connection: close\n\n"
        response += "<html><body><h1>Оценка добавлена!</h1></body></html>"
        conn.sendall(response.encode())

    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)

    print("Сервер запущен. Ожидание подключений...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()


start_server()
