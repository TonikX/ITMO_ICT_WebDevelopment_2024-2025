import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 4096

def build_response(body: bytes) -> bytes:
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        "",
    ]
    header_bytes = "\r\n".join(headers).encode("utf-8")
    return header_bytes + body

def main():
    html_path = Path("index.html")
    if not html_path.exists():
        raise FileNotFoundError("Файл index.html не найден рядом с сервером.")

    body = html_path.read_bytes()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"HTTP-сервер запущен на http://{HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            with conn:
                request = conn.recv(BUFFER_SIZE)
                print(f"Запрос от {addr}:\n{request.decode('utf-8', errors='ignore')}")
                response = build_response(body)
                conn.sendall(response)

if __name__ == "__main__":
    main()
