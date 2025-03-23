import socket
import threading
import urllib.parse

# Параметры сервера
HOST = 'localhost'  # Адрес хоста (127.0.0.1 / для локальных соединений)
PORT = 8085  # Порт, на котором будет работать сервер

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}...")

# Словарь для хранения оценок / ключи – названия предметов, а значения – списки оценок
grades = {}


# Обработка запроса клиента
def handle_client(client_connection):
    # Получаем запрос от клиента используя метод recv()
    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Обрабатываем GET и POST запросы
    if request.startswith('POST'):
        # Извлекаем данные из POST-запроса
        body = request.split('\r\n\r\n')[1]  # Разделитель между заголовками HTTP-запроса и его телом, берем второе
        body = urllib.parse.unquote_plus(body)  # Декодируем данные и заменяем плюс

        discipline, grade = body.split('&')
        discipline = discipline.split('=')[1]
        grade = grade.split('=')[1]

        # Добавляем оценку в список для этой дисциплины
        if discipline not in grades:
            grades[discipline] = []
        grades[discipline].append(grade)

        # Формируем HTTP-ответ с заголовками и HTML-контентом
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        response += "<html><body><h1>Данные успешно сохранены!</h1><a href='/'>Вернуться на главную</a></body></html>"

    elif request.startswith('GET'):
        # Формируем HTML-ответ с оценками
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        response += "<html><body><h1>Оценки по дисциплинам</h1><ul>"

        for discipline, grades_list in grades.items():
            grades_str = ", ".join(grades_list)
            response += f"<li>{discipline}: {grades_str}</li>"

        # Форма для добавления новой оценки
        response += """
            <h2>Добавить оценку</h2>
            <form method="POST" action="/">
                <label for="discipline">Дисциплина:</label>
                <input type="text" id="discipline" name="discipline" required><br><br>
                <label for="grade">Оценка:</label>
                <input type="text" id="grade" name="grade" required><br><br>
                <input type="submit" value="Добавить">
            </form>
        """

        response += "</body></html>"

    else:
        # Если запрос не поддерживается
        response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
        response += "<html><body><h1>Неподдерживаемый запрос</h1></body></html>"

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode('utf-8'))

    # Закрываем соединение
    client_connection.close()


while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Обрабатываем клиента в отдельном потоке
    client_thread = threading.Thread(target=handle_client, args=(client_connection,))
    client_thread.start()
