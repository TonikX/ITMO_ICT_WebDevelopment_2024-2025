import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12347))
server.listen()

clients = []

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            for c in clients:
                if c != conn:
                    c.send(msg)
        except:
            break

    clients.remove(conn)
    conn.close()

print("Чат-сервер запущен...")

while True:
    conn, addr = server.accept()
    print("Подключился:", addr)
    clients.append(conn)

    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()
x