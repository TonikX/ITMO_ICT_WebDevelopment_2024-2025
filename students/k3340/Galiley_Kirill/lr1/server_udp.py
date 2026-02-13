import socket

HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    print("Received from client:", data.decode("utf-8"))
    reply = "Hello, client"
    sock.sendto(reply.encode("utf-8"), addr)
