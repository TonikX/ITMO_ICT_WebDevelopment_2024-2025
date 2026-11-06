import socket
import threading

HOST = "127.0.0.1"
PORT = 12347

clients = {}
lock = threading.Lock()


def broadcast(message, sender=None):
    with lock:
        recipients = [
            client for client in clients
            if client != sender
        ]

    for client in recipients:
        try:
            client.sendall((message + "\n").encode())
        except OSError:
            pass


def handle_client(conn, address):
    name = None

    try:
        with conn:
            reader = conn.makefile("r", encoding="utf-8")
            name = reader.readline().strip()

            if not name:
                return

            with lock:
                clients[conn] = name

            print(f"{name} подключился: {address}")
            broadcast(f"{name} вошёл в чат", conn)

            for line in reader:
                message = line.strip()

                if message == "/exit":
                    break

                if message:
                    print(f"{name}: {message}")
                    broadcast(f"{name}: {message}", conn)

    except (OSError, UnicodeError):
        pass

    finally:
        with lock:
            clients.pop(conn, None)

        if name:
            print(f"{name} отключился")
            broadcast(f"{name} вышел из чата")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Чат-сервер запущен на {HOST}:{PORT}")

while True:
    conn, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, address),
        daemon=True
    )
    thread.start()