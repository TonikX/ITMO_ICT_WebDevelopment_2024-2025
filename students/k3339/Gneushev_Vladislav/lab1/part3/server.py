import socket

from constants import SERVER_HOST, SERVER_PORT


def get_html():
    with open("part3/static/index.html", "r") as f:
        return f.read()


html_str = get_html()


def create_message_from_file(file_path: str):
    with open(file_path, "r") as f:
        return f.read()


def receive_message(sock):
    try:
        data, addr = sock.recvfrom(1024)
        udata = data.decode("utf-8")
        print(f"Received message from {addr}: {udata}")
        return udata, addr
    except socket.timeout:
        return None, None


def send_message(sock, message: str, addr):
    sock.sendto(message.encode("utf-8"), addr)
    print(f"Sent message to {addr}: {message}")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.settimeout(1.0)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        message, addr = receive_message(s)
        if message:
            send_message(
                sock=s,
                message=html_str,
                addr=addr
            )
