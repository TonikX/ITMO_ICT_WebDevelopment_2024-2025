import socket

HOST = 'localhost'
PORT = 8080

# Создаем TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Сервер запущен на http://{HOST}:{PORT}")

while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    # Получаем запрос от клиента
    request = client_connection.recv(1024).decode()
    print(f"Запрос:\n{request}")

    # Загружаем HTML из файла index.html
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        body = "<h1>Файл index.html не найден</h1>"

    # Формируем HTTP-ответ
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n"
        f"{body}"
    )

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())
    client_connection.close()
