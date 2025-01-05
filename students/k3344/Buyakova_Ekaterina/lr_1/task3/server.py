import socket

# Путь к файлу с HTML-контентом
HTML_FILE_PATH = 'index.html'

# Функция для загрузки содержимого HTML-файла
def load_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>404 Not Found</h1></body></html>"

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

# Начинаем слушать входящие подключения
server_socket.listen(5)
print("Server starts on port 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Connection from {client_address}')

    # Получаем запрос от клиента
    request = client_connection.recv(2048).decode()
    print(f'Request from client:\n{request}')

    # Загружаем содержимое HTML файла
    html_content = load_html(HTML_FILE_PATH)

    # Формируем HTTP-ответ с заголовками и HTML-контентом
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем HTTP-ответ клиенту частями, если данные больше буфера
    client_connection.sendall(http_response.encode('utf-8'))

    # Закрываем соединение с клиентом
    client_connection.close()
