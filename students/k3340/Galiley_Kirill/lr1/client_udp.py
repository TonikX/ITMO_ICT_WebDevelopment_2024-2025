import socket

HOST = "127.0.0.1"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "Hello, server"
sock.sendto(msg.encode("utf-8"), (HOST, PORT))

data, _ = sock.recvfrom(1024)
print("Received from server:", data.decode("utf-8"))

sock.close()
