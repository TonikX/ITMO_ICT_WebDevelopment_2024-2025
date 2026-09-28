import socket
import threading

HOST = "127.0.0.1"
PORT = 50003

COLORS = {
    "1": "\033[31m",  # красный
    "2": "\033[32m",  # зелёный
    "3": "\033[33m",  # жёлтый
    "4": "\033[34m",  # синий
    "5": "\033[35m",  # пурпурный
    "6": "\033[36m",  # голубой
    "7": "\033[37m",  # белый
    "8": "\033[38;5;208m",  # оранжевый
}
RESET = "\033[0m"
BOLD = "\033[1m"

clients = []  # список кортежей (conn, имя, цвет)
clients_lock = threading.Lock()


def broadcast(message, sender_conn):
    with clients_lock:
        for conn, name, color in clients:
            if conn is not sender_conn:
                conn.send(message.encode())


def handle_client(conn, address):
    name, color_num = conn.recv(1024).decode().split("|")
    color = COLORS.get(color_num, RESET)

    with clients_lock:
        clients.append((conn, name, color))

    print(f"{name} подключился ({address})")
    broadcast(f"{BOLD}{color}{name} ВОШЁЛ В ЧАТ{RESET}", conn)

    while True:
        data = conn.recv(1024).decode()

        if not data or data == "/exit":
            break

        broadcast(f"{color}{name}{RESET}: {data}", conn)

    with clients_lock:
        clients.remove((conn, name, color))

    print(f"{name} отключился")
    broadcast(f"{BOLD}{color}{name} ВЫШЕЛ ИЗ ЧАТА{RESET}", conn)
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.settimeout(0.5)  # чтобы accept() не блокировал Ctrl+C навсегда
print(f"Чат-сервер запущен на {HOST}:{PORT}")

try:
    while True:
        try:
            conn, address = server.accept()
        except socket.timeout:
            continue

        thread = threading.Thread(target=handle_client, args=(conn, address), daemon=True)
        thread.start()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server.close()
