import socket
import threading

HOST = "127.0.0.1"
PORT = 5004

clients = []
lock = threading.Lock()

def broadcast(message, sender_sock):
    with lock:
        for c in clients:
            if c is not sender_sock:
                try:
                    c.sendall(message)
                except:
                    pass

def handle_client(conn, addr):
    print("New connection:", addr)
    with lock:
        clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = f"[{addr[0]}:{addr[1]}] ".encode("utf-8") + data
            broadcast(msg, conn)
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print("Disconnected:", addr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Chat server on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()
