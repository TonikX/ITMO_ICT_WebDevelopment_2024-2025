import socket
from constants import SERVER_HOST, SERVER_PORT


def get_html():
    with open("static/index.html", "r") as f:
        return f.read()


def create_message_from_file(file_path: str):
    with open(file_path, "r") as f:
        html_code = f.read()
    return '\n'.join([
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {len(html_code)}",
        "",
        html_code
    ])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            request = conn.recv(1024).decode('utf-8')
            if request:
                response = create_message_from_file("static/index.html")
                conn.sendall(response.encode("utf-8"))
