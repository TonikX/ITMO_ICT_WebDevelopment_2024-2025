import socket

con_sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con_sever.bind(('localhost', 7090))
con_sever.listen(1)

while True:
    clin_conn, clin_addr = con_sever.accept()

    request = clin_conn.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    with open('index.html', 'r') as file:
        content = file.read()

    http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            + content
    )

    # Отправляем HTTP-ответ клиенту
    clin_conn.sendall(http_response.encode())

    # Закрываем соединение
    clin_conn.close()
