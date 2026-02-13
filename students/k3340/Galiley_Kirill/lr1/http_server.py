import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 5002

def build_response(body: bytes) -> bytes:
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"HTTP server on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(1024)
            print("Request from", addr)
            body = Path("index.html").read_bytes()
            response = build_response(body)
            conn.sendall(response)
