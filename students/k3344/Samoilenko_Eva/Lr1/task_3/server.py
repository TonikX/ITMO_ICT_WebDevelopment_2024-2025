import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_address = ('localhost', 8080)
serv_sock.bind(serv_address)
serv_sock.listen(1)

while True:
    conn, cl_address = serv_sock.accept()
    data = conn.recv(1024).decode()

    with open('index.html', 'r') as file:
        html_content = file.read()

    message = f"HTTP/1.1 200 OK\r\n" \
              f"Content-Type: text/html\r\n" \
              f"Content-Length: {len(html_content)}\r\n" \
              f"\r\n" \
              f"{html_content}"

    conn.sendall(message.encode())

    conn.close()
