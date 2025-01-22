import socket

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"HTTP is running on {HOST}:{PORT}...")

with open('index.html', 'r') as file:
    html_content = file.read()

while True:
    client, client_address = server_socket.accept()
    print(f'Connection from {client_address}')

    request = client.recv(1024).decode()
    print(f'Request of client:\n{request}')

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=ASCII\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client.sendall(http_response.encode())

    client.close()
