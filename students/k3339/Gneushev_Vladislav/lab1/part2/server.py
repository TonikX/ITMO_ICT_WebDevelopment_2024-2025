import socket

from constants import SERVER_HOST, SERVER_PORT
from pythagorean import parse_pythagorean_params, calculate_pythagorean


def receive_message(conn):
    try:
        data = conn.recv(1024)
        udata = data.decode("utf-8")
        if not udata:
            return None
        print(f"Received message: {udata}")
        return udata
    except socket.timeout:
        return None


def send_message(conn, message: str):
    conn.sendall(message.encode("utf-8"))
    print(f"Sent message: {message}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen()
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn:
        while True:
            conn.settimeout(1.0)
            message = receive_message(conn)
            if message:
                try:
                    pythagorean_params = parse_pythagorean_params(message)
                except ValueError:
                    response = "Invalid input"
                else:
                    response = str(calculate_pythagorean(pythagorean_params))
                send_message(conn, response)
