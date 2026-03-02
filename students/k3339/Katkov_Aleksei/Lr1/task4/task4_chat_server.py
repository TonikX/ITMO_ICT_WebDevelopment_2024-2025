import socket
import threading

HOST = "127.0.0.1"
PORT = 14000
BUFFER_SIZE = 1024

clients = []
lock = threading.Lock()


def broadcast(message: bytes):
    # Отправляем сообщение всем подключенным пользователям
    with lock:
        for client in clients:
            try:
                client.sendall(message)
            except OSError:
                pass


def handle_client(conn: socket.socket, addr):
    print(f"Клиент подключился: {addr}")

    with lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break

            text = data.decode("utf-8").rstrip()
            if not text:
                continue

            formatted = f"[{addr[0]}:{addr[1]}] {text}\n".encode("utf-8")
            print(formatted.decode("utf-8"), end="")
            broadcast(formatted)
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"Клиент отключился: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер чата успешно запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    main()
