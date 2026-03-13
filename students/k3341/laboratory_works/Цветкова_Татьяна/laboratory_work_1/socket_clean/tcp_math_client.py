import socket

HOST = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Введите команду:")
print("PYTH a b")
print("QUAD a b c")
print("TRAP a b h")
print("PARA a h")

while True:
    cmd = input("> ")
    client.send(cmd.encode())
    data = client.recv(1024).decode()
    print("Ответ сервера:", data)