import socket


def handle_request(client_socket):
    try:
        with open("index.html", "r") as html_file:
            content = html_file.read()

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
            f"{content}"
        )
    except FileNotFoundError:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            "\r\n"
            "<html><body><h1>404 Not Found</h1></body></html>"
        )

    client_socket.send(response.encode())


def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        handle_request(client_socket)
        client_socket.close()


if __name__ == "__main__":
    start_server()