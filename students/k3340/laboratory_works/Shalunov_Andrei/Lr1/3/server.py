import socket

HOST = 'localhost'
PORT = 8080

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen()
html_content = open('index.html').read()

while True:
    client_connection, client_address = server_sock.accept()
    request = client_connection.recv(1024).decode()
    print(f"Запрос от клиента:\n{request}")

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode())
    client_connection.close()
