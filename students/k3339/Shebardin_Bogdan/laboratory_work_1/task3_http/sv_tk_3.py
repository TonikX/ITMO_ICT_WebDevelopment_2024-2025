import socket

HOST = "127.0.0.1"
PORT = 8080

def build_response(body: bytes) -> bytes:
    """Собирает HTTP-ответ по всем правилам."""
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Сервер запущен на http://{HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"Подключение от {client_addr}")

            try:
                request = client_sock.recv(4096)
                print("Запрос:")
                print(request.decode("utf-8", errors="replace"))

                with open("index.html", "rb") as f:
                    body = f.read()

                response = build_response(body)
                client_sock.sendall(response)
            finally:
                client_sock.close()
    except KeyboardInterrupt:
        print("\nОстановка сервера")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()