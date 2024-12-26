import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 8080))

    server_socket.listen(1)
    client_connection, client_address = server_socket.accept()

    with client_connection:
        print(f'Подключение от {client_address}')

        data = client_connection.recv(1024)

        with open('index.html', 'r') as file:
            html_content = file.read()

        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html_content
        )

        client_connection.sendall(http_response.encode())
