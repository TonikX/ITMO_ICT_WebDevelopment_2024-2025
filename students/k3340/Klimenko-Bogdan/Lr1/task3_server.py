import socket

# Настройки сервера
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024

# Создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # избежать ошибки "Address already in use"
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"HTTP-сервер запущен на http://{HOST}:{PORT}/")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Подключение от {addr}")

        # Получаем запрос от клиента (браузера) — можно не использовать, но прочитать нужно
        request = conn.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Запрос:\n{request.splitlines()[0]}")  # печатаем только первую строку

        # Пытаемся прочитать файл index.html
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            status_line = "HTTP/1.1 200 OK\r\n"
        except FileNotFoundError:
            html_content = "<h1>404 Not Found</h1><p>Файл index.html не найден.</p>"
            status_line = "HTTP/1.1 404 Not Found\r\n"

        # Формируем HTTP-ответ
        headers = (
            f"Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        http_response = status_line + headers + html_content

        # Отправляем ответ
        conn.sendall(http_response.encode('utf-8'))
        conn.close()
        print("Ответ отправлен, соединение закрыто\n")

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()