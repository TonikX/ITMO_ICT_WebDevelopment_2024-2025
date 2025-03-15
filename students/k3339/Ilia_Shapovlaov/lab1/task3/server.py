from socket import socket, AF_INET, SOCK_STREAM


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)

    while True:
        with server_socket.accept()[0] as client_socket:
            try:
                with open("index.html", "r") as file:
                    html_content = file.read()
                    response_parts = [
                        "HTTP/1.1 200 OK\r\n",
                        "Content-Type: text/html; charset=UTF-8\r\n",
                        f"Content-Length: {len(html_content)}\r\n",
                        "\r\n",
                        html_content,
                    ]

                response = "".join(response_parts)
                client_socket.sendall(response.encode("utf-8"))
            except Exception as e:
                error_message = f"HTTP/1.1 500 Internal Server Error\r\n"
                client_socket.sendall(error_message.encode("utf-8"))
