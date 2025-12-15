from __future__ import annotations
import socket, pathlib
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080
INDEX = pathlib.Path(__file__).with_name("index.html")

def http_response(status: str, headers: dict[str, str], body: bytes) -> bytes:
    head = f"HTTP/1.1 {status}\r\n" + "".join(f"{k}: {v}\r\n" for k, v in headers.items()) + "\r\n"
    return head.encode("utf-8") + body

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"[{datetime.now():%H:%M:%S}] Serving index.html on http://{HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            with conn:
                req = conn.recv(65536)
                if not req:
                    continue
                if INDEX.exists():
                    body = INDEX.read_bytes()
                    resp = http_response("200 OK", {
                        "Content-Type": "text/html; charset=utf-8",
                        "Content-Length": str(len(body)),
                        "Connection": "close",
                    }, body)
                else:
                    msg = b"<h1>404 Not Found</h1>"
                    resp = http_response("404 Not Found", {
                        "Content-Type": "text/html; charset=utf-8",
                        "Content-Length": str(len(msg)),
                        "Connection": "close",
                    }, msg)
                conn.sendall(resp)

if __name__ == "__main__":
    main()
