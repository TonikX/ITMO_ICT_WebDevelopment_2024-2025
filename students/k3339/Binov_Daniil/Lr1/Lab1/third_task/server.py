import socket

host = '127.0.0.1'
port = 8080
buffer_size = 1024
max_connections_count = 1

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(max_connections_count)
    print(f"Сервер запущен на http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")

        request = client_socket.recv(buffer_size).decode('utf-8')
        print(f"Получен запрос:\n{request}")

        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content)}\r\n"
        response += f"\r\n"
        response += html_content

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()