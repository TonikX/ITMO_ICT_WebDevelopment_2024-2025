import socket
import threading


HOST = 'localhost'
PORT = 9090

clients = []

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {addr} подключился.")
    connected = True
    while connected:
        try:
            message = conn.recv(1024)
            if message:
                print(f"[{addr}] {message.decode()}")
                broadcast(message, conn)
            else:
                connected = False
        except:
            connected = False

    conn.close()
    clients.remove(conn)
    print(f"[ОТКЛЮЧЕНИЕ] {addr} отключился.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ЗАПУЩЕН] Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[АКТИВНЫЕ ПОДКЛЮЧЕНИЯ] {threading.active_count() - 1}")

start_server()