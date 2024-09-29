import socket


def create_server(host='127.0.0.1', port=8081):
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Устанавливаем опцию повторного использования адреса
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))

    # Начинаем прослушивание входящих соединений
    server_socket.listen(1)
    print(f"Сервер запущен на http://{host}:{port}")

    while True:
        # Принимаем соединение от клиента
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")

        # Получаем запрос от клиента
        request = client_socket.recv(1024).decode()
        print(f"Запрос: {request}")

        # Читаем содержимое файла index.html
        try:
            with open('index.html', 'r') as file:
                html_content = file.read()
        except FileNotFoundError:
            html_content = "<h1>404 Not Found</h1>"

        # Формируем HTTP-ответ
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{html_content}"

        # Отправляем ответ клиенту
        client_socket.sendall(response.encode())

        # Закрываем соединение с клиентом
        client_socket.close()


if __name__ == "__main__":
    create_server()