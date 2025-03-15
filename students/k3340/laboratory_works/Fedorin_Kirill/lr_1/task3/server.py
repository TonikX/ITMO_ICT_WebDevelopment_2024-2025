import socket


def start_server() -> None:
    # Создаём TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print('HTTP сервер запущен на http://localhost:8080')

    while True:
        # Принимаем входящее соединение
        client_connection, client_address = server_socket.accept()
        print(f'Клиент подключён: {client_address}')

        # Читаем запрос от клиента
        request = client_connection.recv(1024).decode()
        print(f'Получен запрос:\n{request}')

        # Загружаем HTML-страницу из файла
        try:
            with open('index.html') as file:
                html_content = file.read()

            # Формируем HTTP-ответ
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html_content)}\r\n\r\n{html_content}'
        except FileNotFoundError:
            # Если файл не найден, возвращаем ошибку 404
            response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>404 Not Found</h1><p>index.html не найден</p>'

        # Отправляем ответ клиенту
        client_connection.sendall(response.encode())
        client_connection.close()


if __name__ == '__main__':
    start_server()
