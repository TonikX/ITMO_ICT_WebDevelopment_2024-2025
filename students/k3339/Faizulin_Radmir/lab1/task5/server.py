import socket
import threading

# Настройки сервера
HOST = '127.0.0.1'  # Адрес сервера
PORT = 8080  # Порт сервера

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()  # Ограничиваем количество одновременных подключений

print(f"Сервер запущен на http://{HOST}:{PORT}")

# Словарь для хранения дисциплин и оценок
grades = {}


def handle_request(client_socket):
    # Получаем данные от клиента
    request_data = client_socket.recv(4096).decode()
    print(f"Получен запрос:\n{request_data}")

    # Разбираем HTTP-заголовки
    headers = request_data.split('\n')
    method = headers[0].split()[0]  # GET или POST
    path = headers[0].split()[1]  # Путь запроса

    # Обработка GET-запроса
    if method == 'GET' and path == '/':
        # Формируем HTML-страницу с оценками
        html_content = "<html><body><h1>Оценки</h1><ul>"
        for subject, grade in grades.items():
            html_content += f"<li>{subject}: {grade}</li>"
        html_content += "</ul></body></html>"

        # Отправляем HTTP-ответ с указанием кодировки
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html; charset=utf-8\n\n"  # Указываем кодировку
            f"{html_content}"
        )
        client_socket.send(response.encode())

    # Обработка POST-запроса
    elif method == 'POST' and path == '/add':
        # Извлекаем данные из тела запроса
        body = request_data.strip().split('\n')[-1]
        subject = body.split('&')[0].split('=')[1]
        grade = body.split('&')[1].split('=')[1]

        # Сохраняем данные в словарь
        grades[subject] = grade

        # Отправляем HTTP-ответ
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/plain; charset=utf-8\n\n"  # Указываем кодировку
            "Данные успешно добавлены!"
        )
        client_socket.send(response.encode())

    # Если запрос не распознан
    else:
        response = (
            "HTTP/1.1 404 Not Found\n"
            "Content-Type: text/plain; charset=utf-8\n\n"  # Указываем кодировку
            "Страница не найдена"
        )
        client_socket.send(response.encode())

    # Закрываем соединение
    client_socket.close()


# Основной цикл сервера
while True:
    # Принимаем подключение
    client_socket, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    # Обрабатываем запрос
    client_thread = threading.Thread(target=handle_request, args=(client_socket,))
    client_thread.start()
