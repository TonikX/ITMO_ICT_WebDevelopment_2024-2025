import socket
import threading

HOST = "127.0.0.1"
PORT = 5004

def receive_loop(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=receive_loop, args=(s,), daemon=True).start()
    print("Connected to chat. Type messages ('/quit' to exit):")
    while True:
        msg = input()
        if msg.lower() == "/quit":
            break
        if msg:
            s.sendall(msg.encode("utf-8"))
