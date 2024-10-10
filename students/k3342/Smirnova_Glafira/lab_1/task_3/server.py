import socket


def load_html():
    try:
        with open('index.html', 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>404 Not Found</h1></body></html>"


def handle_client(client_socket):
    try:
        html_content = load_html()

        response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                "\r\n"
                + html_content
        )
        client_socket.sendall(response.encode())

    finally:
        client_socket.close()


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер запущен на {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket)
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server('127.0.0.1', 8080)
