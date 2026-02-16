import socket
import threading

clients = {}  # словарь: conn -> имя

def handle_client(conn, addr):
    try:
        nickname = conn.recv(1024).decode("utf-8", errors="ignore") # первым делом получаем ник от клиента
        clients[conn] = nickname
        print(f"[+] {nickname} подключился с {addr}")

        broadcast(f"📢 {nickname} вошёл в чат", conn) # рассылаем всем сообщение о подключении

        while True:
            msg = conn.recv(1024).decode("utf-8", errors="ignore")
            if not msg:
                break
            print(f"[{nickname}]: {msg}")
            broadcast(f"[{nickname}]: {msg}", conn)

    except:
        pass
    finally:
        if conn in clients: # отключение клиента
            name = clients[conn]
            print(f"[-] {name} отключился")
            broadcast(f"📢 {name} покинул чат", conn)
            del clients[conn]
        conn.close()

def broadcast(message, sender_conn=None):
    """Рассылка всем клиентам, кроме отправителя"""
    for c in list(clients.keys()):
        if c != sender_conn:
            try:
                c.send(message.encode("utf-8", errors="ignore"))
            except:
                c.close()
                del clients[c]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 12345))
sock.listen()

print("Сервер чата запущен...")

while True:
    conn, addr = sock.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
