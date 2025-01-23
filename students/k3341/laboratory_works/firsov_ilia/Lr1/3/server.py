import socket


def load_html(file_path):
    with open(file_path, 'r') as file:
        return file.read()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
server_socket.bind(server_address)
server_socket.listen(1)

print("Server is running and waiting for connection...")

while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"Connected client: {client_address}")

        html_content = load_html('static/index.html')

        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html_content)}\r\n\r\n{html_content}"

        connection.sendall(http_response.encode())
    finally:
        connection.close()
