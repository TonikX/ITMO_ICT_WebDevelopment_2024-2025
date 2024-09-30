import socket

HOST = 'localhost'
PORT = 9000
BUFF_SIZE = 1024
CONNECTIONS = 5


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(CONNECTIONS)

    print(f"Server online on http://{HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_socket.recv(BUFF_SIZE)

        with open('index.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "\r\n"
                + html_content
        )
        client_socket.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    start_server()
