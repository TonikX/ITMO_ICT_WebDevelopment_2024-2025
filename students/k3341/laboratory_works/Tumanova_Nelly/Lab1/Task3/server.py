import socket

SERVER_ADDR = ("", 9090)
INDEX_FILE = 'index.html'


def load_index_html():
    """Читает содержимое index.html из файла."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def build_http_response(body: str, status: str = "200 OK") -> bytes:
    """Формирует корректное HTTP-сообщение."""
    body_bytes = body.encode('utf-8')
    headers = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return headers.encode('utf-8') + body_bytes

def handle_client(sock, addr):
    data = sock.recv(1024)
    if not data:
        print(f"[*] Client {addr[0]}{addr[1]} disconnected")
        return

    request = data.decode("utf-8")
    first_line = request.split('\r\n')[0] if request else "(empty)"
    print(f"[Message from {addr[0]}:{addr[1]}] {first_line}")

    try:
        html = load_index_html()
        response = build_http_response(html)
    except FileNotFoundError:
        response = build_http_response("<h1>404 Not Found</h1>",
                                       status="404 Not Found")

    sock.sendall(response)


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # чтобы сразу после перезапуска сервера заново привязать его к тому же порту без ошибки
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen(socket.SOMAXCONN)

    print(f"[*] TCP-server started on {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Client {client_address[0]}{client_address[1]} connected")

            try:
                handle_client(client_socket, client_address)
            except (ConnectionResetError, BrokenPipeError) as e:
                print(f"[Error] {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("[*] TCP-server stopped")
    finally:
        server_socket.close()
