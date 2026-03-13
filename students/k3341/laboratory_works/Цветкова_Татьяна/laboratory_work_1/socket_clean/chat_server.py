import socket
import threading

HOST = "127.0.0.1"
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            for c in clients:
                if c != client:
                    c.send(msg)
        except:
            break

    clients.remove(client)
    client.close()

print("Чат-сервер запущен...")

while True:
    client, addr = server.accept()
    print("Подключился:", addr)
    clients.append(client)
    threading.Thread(target=handle, args=(client,), daemon=True).start()