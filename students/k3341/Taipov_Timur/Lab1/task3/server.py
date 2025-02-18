import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8082))
server_socket.listen(1)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    request = client_socket.recv(1024).decode('utf-8')
    print(f"Request:\n{request}")

    with open("index.html", "r") as file:
        html_content = file.read()

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{html_content}"
    )

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
