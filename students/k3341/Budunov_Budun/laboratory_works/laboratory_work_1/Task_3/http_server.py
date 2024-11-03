import socket


def start_server():
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    # Ожидаем подключения клиентов
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключения...")

    while True:
        # Принимаем соединение от клиента
        client_connection, client_address = server_socket.accept()
        try:
            print(f"Подключение от клиента: {client_address}")

            # Читаем и выводим запрос от клиента (GET-запрос)
            request = client_connection.recv(1024).decode()
            print("Получен запрос от клиента:", request)

            # Проверяем, что запрос начинается с "GET"
            if request.startswith("GET"):
                # Загружаем HTML-файл
                try:
                    with open("index.html", "r", encoding="utf-8") as file:
                        html_content = file.read()
                except FileNotFoundError:
                    # Если файл не найден, отправляем сообщение об ошибке
                    html_content = "<html><body><h1>404 Not Found</h1></body></html>"

                # Формируем корректный HTTP-ответ
                http_response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content)}

{html_content}
"""
            else:
                # Если запрос не GET, отправляем сообщение об ошибке
                http_response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid request."

            # Отправляем HTTP-ответ клиенту
            client_connection.sendall(http_response.encode())
            print("HTTP-ответ отправлен клиенту.")

        finally:
            # Закрываем соединение с клиентом
            client_connection.close()


if __name__ == "__main__":
    start_server()
