import socket

with open('index.html', 'r') as file:
    html = file.read()
http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{html}"
)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen()
    print("Сервер запущен и ожидает подключения на http://localhost:8080")
    while True:
        client, address = server_socket.accept()
        print(f"Получен запрос:\n{client.recv(1024).decode()}")
        client.sendall(http_response.encode())
        client.close()
