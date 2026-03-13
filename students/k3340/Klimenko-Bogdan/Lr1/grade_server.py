import socket
import urllib.parse
import json
import os

# ================== НАСТРОЙКИ ==================
HOST = '127.0.0.1'
PORT = 8081
GRADES_FILE = 'grades.json'

# ================== РАБОТА С ФАЙЛОМ ==================
def load_grades():
    if os.path.exists(GRADES_FILE):
        with open(GRADES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_grades(grades):
    with open(GRADES_FILE, 'w', encoding='utf-8') as f:
        json.dump(grades, f, ensure_ascii=False, indent=2)

grades = load_grades()

# ================== HTML-ШАБЛОН ==================
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Оценки по дисциплинам</title>
    <style>
        table {{ border-collapse: collapse; width: 50%; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        form {{ margin-top: 20px; }}
    </style>
</head>
<body>
    <h1>Список оценок</h1>
    <table>
        <tr><th>Дисциплина</th><th>Оценка</th></tr>
        {rows}
    </table>
    <h2>Добавить оценку</h2>
    <form method="POST" action="/">
        Дисциплина: <input type="text" name="discipline" required><br>
        Оценка: <input type="number" name="grade" min="1" max="5" required><br>
        <input type="submit" value="Отправить">
    </form>
</body>
</html>
"""

# ================== ЧТЕНИЕ ЗАПРОСА ПОЛНОСТЬЮ ==================
def recv_all(conn):
    """
    Читает все данные из сокета до тех пор, пока не будет получен полный HTTP-запрос.
    Возвращает байтовую строку запроса.
    """
    data = b''
    while True:
        try:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            # Проверяем, получили ли мы конец заголовков (двойной перевод строки)
            if b'\r\n\r\n' in data:
                # Заголовки получены, теперь нужно определить, есть ли тело и сколько байт читать
                headers_end = data.find(b'\r\n\r\n') + 4
                headers = data[:headers_end].decode('utf-8', errors='ignore')
                # Ищем Content-Length
                content_length = 0
                for line in headers.split('\r\n'):
                    if line.lower().startswith('content-length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                # Если тело ожидается и мы уже получили его полностью – выходим
                if len(data) - headers_end >= content_length:
                    break
                # Иначе продолжаем читать, пока не получим нужное количество байт
        except socket.timeout:
            # Таймаут не устанавливаем, чтобы избежать ошибок
            break
    return data

# ================== ПАРСИНГ POST-ДАННЫХ ==================
def parse_post_data(data):
    """Разбирает строку вида 'discipline=Math&grade=5' в словарь."""
    params = urllib.parse.parse_qs(data)
    discipline = params.get('discipline', [''])[0]
    grade = params.get('grade', [''])[0]
    return discipline, grade

# ================== ОБРАБОТКА ЗАПРОСА ==================
def handle_request(request_data):
    """
    Обрабатывает HTTP-запрос и возвращает кортеж (статус, тело_ответа, доп_заголовки)
    """
    # Разбиваем запрос на строки (первая строка – request line)
    # Сначала декодируем только заголовочную часть для разбора
    # Но проще работать с байтами, но для простоты оставим строку
    # Запрос уже в виде строки, но нужно разделить заголовки и тело
    try:
        # Ищем разделитель между заголовками и телом
        header_end = request_data.find('\r\n\r\n')
        if header_end == -1:
            return "400 Bad Request", "<h1>400 Bad Request (No headers end)</h1>", []

        headers_part = request_data[:header_end]
        body_part = request_data[header_end+4:]

        lines = headers_part.split('\r\n')
        if not lines:
            return "400 Bad Request", "<h1>400 Bad Request</h1>", []

        request_line = lines[0]
        parts = request_line.split()
        if len(parts) < 2:
            return "400 Bad Request", "<h1>400 Bad Request</h1>", []

        method, path = parts[0], parts[1]

        # Игнорируем запросы favicon.ico
        if path == '/favicon.ico':
            return "204 No Content", "", []

        if path != '/':
            return "404 Not Found", "<h1>404 Not Found</h1>", []

        # --- GET запрос ---
        if method == 'GET':
            rows = ''
            for disc, grade in grades:
                rows += f"<tr><td>{disc}</td><td>{grade}</td></tr>\n"
            body = HTML_TEMPLATE.format(rows=rows)
            return "200 OK", body, []

        # --- POST запрос ---
        elif method == 'POST':
            # Извлекаем Content-Length из заголовков
            content_length = 0
            for line in lines:
                if line.lower().startswith('content-length:'):
                    content_length = int(line.split(':')[1].strip())
                    break

            if content_length == 0:
                return "400 Bad Request", "<h1>400 Bad Request (No Content-Length)</h1>", []

            # Тело должно быть уже в body_part, но если его нет (редко), пробуем прочитать ещё
            if len(body_part) < content_length:
                # В реальности мы уже должны были получить всё в recv_all, но на всякий случай
                return "400 Bad Request", "<h1>400 Bad Request (Incomplete body)</h1>", []

            post_data = body_part[:content_length]
            discipline, grade = parse_post_data(post_data)

            if not discipline or not grade:
                return "400 Bad Request", "<h1>Не хватает данных (discipline и grade обязательны)</h1>", []

            try:
                grade = int(grade)
                grades.append((discipline, grade))
                save_grades(grades)
                print(f"Добавлено: {discipline} - {grade}")
                return "303 See Other", "", [("Location", "/")]
            except ValueError:
                return "400 Bad Request", "<h1>Оценка должна быть числом</h1>", []

        else:
            return "405 Method Not Allowed", "<h1>405 Method Not Allowed</h1>", []

    except Exception as e:
        # Если что-то пошло не так, возвращаем 500 с текстом ошибки для отладки
        return "500 Internal Server Error", f"<h1>500 Internal Server Error</h1><p>{e}</p>", []

# ================== ЗАПУСК СЕРВЕРА ==================
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Веб-сервер запущен на http://{HOST}:{PORT}/")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Подключение от {addr}")

        # Устанавливаем небольшой таймаут для предотвращения зависаний, но чтение теперь умное
        conn.settimeout(5.0)

        try:
            # Читаем запрос полностью с помощью recv_all
            raw_request = recv_all(conn)
            if not raw_request:
                conn.close()
                continue

            # Декодируем запрос в строку (ошибки игнорируем)
            request_data = raw_request.decode('utf-8', errors='ignore')

            # Обрабатываем запрос
            status, body, extra_headers = handle_request(request_data)

        except socket.timeout:
            status, body, extra_headers = "408 Request Timeout", "<h1>408 Request Timeout</h1>", []
        except Exception as e:
            status, body, extra_headers = "500 Internal Server Error", f"<h1>500 Internal Server Error</h1><p>{e}</p>", []

        # Формируем ответ
        response_line = f"HTTP/1.1 {status}\r\n"
        headers = [
            f"Content-Length: {len(body.encode('utf-8'))}",
            "Content-Type: text/html; charset=utf-8",
            "Connection: close"
        ]
        for header_name, header_value in extra_headers:
            headers.append(f"{header_name}: {header_value}")

        response = response_line + "\r\n".join(headers) + "\r\n\r\n" + body

        # Отправляем ответ
        conn.sendall(response.encode('utf-8'))
        conn.close()
        print(f"Ответ отправлен со статусом {status}")

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()