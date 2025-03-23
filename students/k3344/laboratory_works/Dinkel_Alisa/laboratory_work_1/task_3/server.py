import socket

# Параметры сервера
HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8080         # Порт, на котором будет работать сервер

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения
server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем запрос от клиента (например, из браузера)
    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Читаем содержимое html-файла
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Формируем HTTP-ответ с заголовками и HTML-контентом
    content_bytes = html_content.encode('utf-8')  # Закодируем строку в байты
    content_length = len(content_bytes)  # Получим корректную длину

    http_response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=UTF-8\r\n"
                        f"Content-Length: {content_length}\r\n"
                        "Connection: close\r\n"
                        "\r\n"
                    ).encode() + content_bytes

    # Отправляем HTTP-ответ клиенту
    client_connection.sendall(http_response)

    # Закрываем соединение
    client_connection.close()
