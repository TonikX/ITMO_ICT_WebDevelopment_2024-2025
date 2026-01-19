from socket import socket, AF_INET, SOCK_STREAM

# Параметры сервера
HOST = 'localhost'
PORT = 8080

# Создаем сокет
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"HTTP сервер запущен на http://{HOST}:{PORT}...")

# Читаем HTML-страницу
with open('index.html', 'r', encoding='utf-8') as file:
    html_bytes = file.read().encode('utf-8')
    content_length = len(html_bytes)

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    try:
        # Читаем запрос (игнорируем его содержимое для этого простого сервера)
        request = client_connection.recv(4096).decode()

        # Формируем HTTP-ответ
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {content_length}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        # Отправляем заголовки
        client_connection.sendall(response_headers.encode('utf-8'))

        # Отправляем тело ответа (HTML-контент)
        client_connection.sendall(html_bytes)

    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
    finally:
        # Закрываем соединение
        client_connection.close()
        print(f'Соединение с {client_address} закрыто')
