import socket
import math

TCP_IP = "127.0.0.1"
TCP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    print("Connection address:", addr)
    data = conn.recv(1024)
    if not data:
        break
    values = data.decode("utf-8").split()[1:]
    a = int(values[0])
    b = int(values[1])
    c = math.sqrt(a**2 + b**2)
    result = "The length of the hypotenuse is: " + str(c)
    conn.sendall(bytes(result, "utf-8"))
    conn.close()