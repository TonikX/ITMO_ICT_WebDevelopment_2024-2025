import socket
import threading

HOST = 'localhost'
PORT = 8080

# Список клиентов в формате {conn: name}
clients = {}

def handle_client(conn, addr):
    try:
        # Первое сообщение от клиента — его имя
        name = conn.recv(1024).decode("utf-8").strip()
        clients[conn] = name
        print(f"[+] {name} подключился из {addr}")

        broadcast(f"{name} вошёл в чат", conn)

        while True:
            message = conn.recv(1024)
            if not message:
                break
            broadcast(f"{name}: {message.decode('utf-8')}", conn)
    except:
        pass
    finally:
        # Если клиент отключился
        if conn in clients:
            print(f"[-] {clients[conn]} отключился")
            broadcast(f"{clients[conn]} покинул чат", conn)
            del clients[conn]
        conn.close()

def broadcast(message, sender_conn=None):
    for client in list(clients.keys()):
        if client != sender_conn:  # не отправляем отправителю
            try:
                client.send(message.encode("utf-8"))
            except:
                del clients[client]
                client.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
