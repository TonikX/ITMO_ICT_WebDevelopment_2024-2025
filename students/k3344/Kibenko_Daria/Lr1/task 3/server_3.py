import socket


# Функция для загрузки содержимого HTML-файла
def load_html():
    with open("index.html", "r") as file:
        return file.read()

# Создание TCP-сервер: Привязываем сервер к адресу и порту и ожидаем подключения
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Сервер запущен и ожидает подключения на порту 8080...")

while True:
    # Принимаем подключение от клиента
    client_socket, addr = server_socket.accept()
    print(f"Клиент {addr} подключился.")

    # Получаем запрос от клиента
    request = client_socket.recv(1024).decode()
    print(f"Получен запрос:\n{request}")

    # Загружаем содержимое HTML-файла
    html_content = load_html()

    # Формируем HTTP-ответ
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{html_content}"
    )

    client_socket.sendall(http_response.encode())

    client_socket.close()
