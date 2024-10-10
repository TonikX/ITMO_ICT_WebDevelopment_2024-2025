import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 2024))
sock.listen(0)
print("Server listening on port 2024")

with open("index.html", encoding='utf-8') as file:
    page = file.read()

while True:
    client_socket, client_address = sock.accept()
    print("Got connection from", client_address)

    client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{page}".encode())
