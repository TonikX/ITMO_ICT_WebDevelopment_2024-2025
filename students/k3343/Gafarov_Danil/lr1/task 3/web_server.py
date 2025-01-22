import socket


HOST = 'localhost'
PORT = 8080
# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(50)
print(f"HTTP сервер запущен на http://{HOST}:{PORT}...")

# HTML-страница, которая будет отображаться в браузере
html_content = open("index.html", "r", encoding="utf-8").read()

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Формируем HTTP-ответ с заголовками и HTML-контентом
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем HTTP-ответ клиенту
    client_connection.sendall(http_response.encode())

    client_connection.close()