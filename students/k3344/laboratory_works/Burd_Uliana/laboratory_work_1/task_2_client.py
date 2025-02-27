import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5005

a = input("Enter the length of the first cathetus: ")
b = input("Enter the length of the second cathetus: ")

MESSAGE = "PYTHAGOREAN_THEOREM " + a + " " + b

print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.sendall(bytes(MESSAGE, "utf-8"))

data = sock.recv(1024)
print("received message:", data.decode("utf-8"))

sock.close()