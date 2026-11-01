import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

clients = {}
clients_lock = threading.Lock()

def broadcast(msg: str, sender_sock=None):
    data = (msg + '\n').encode("utf-8")
    with clients_lock:
        targets = list(clients.keys())
    for sock in targets:
        if sock is sender_sock:
            continue
        try:
            sock.sendall(data)
        except OSError:
            remove_client(sock)

def remove_client(sock):
    with clients_lock:
        name = clients.pop(sock, None)
    if name:
        print(f"[SERVER] {name} has disconnected")
        broadcast(f"*** {name} покинула чат ***")
    try:
        sock.close
    except OSError:
        pass

def handle_client(sock, addr):
    print(f"[SERVER] {addr} has connected")
    try:
        name = sock.recv(1024).decode("utf-8").strip()
        if not name:
            name = f"user_{addr}"

        with clients_lock:
            clients[sock] = name

        print(f"[SERVER] {name} has connected to chat")
        broadcast(f"*** {name} вошел в чат ***")
        sock.sendall(f"Добро пожаловать {name}!\n".encode("utf-8"))


        while True:
            data = sock.recv(4096)
            if not data:
                break
            text = data.decode("utf-8").strip()
            if not text:
                continue

            if text == "/quit":
                break
            if text == "/users":
                with clients_lock:
                    names = ", ".join(clients.values())
                sock.sendall(f"В чате {names}!\n".encode("utf-8"))
                continue


            print(f"[{name}] {text}")
            broadcast(f"{name}: {text}", sender_sock=sock)
    except (ConnectionResetError, OSError):
        pass
    finally:
        remove_client(sock)


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f"[SERVER] запузен на {HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            t = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr),
                daemon = True,
            )
            t.start()
    except KeyboardInterrupt:
        print(f"\n[SERVER] остановка")
    finally:
        server_sock.close()


if __name__ == "__main__":
    main()








