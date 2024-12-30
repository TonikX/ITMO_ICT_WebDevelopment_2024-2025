import socket
HOST, PORT, max_users = 'localhost', 1235, 5


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with open("index.html", "r") as file:
        file_content = file.read()
    s.bind((HOST, PORT))
    s.listen(max_users)
    print(f"Сервер запущен на {HOST}:{PORT}")
    client_socket, client_address = s.accept()
    print(f"Клиент подключился: {client_address}")
    client_socket.send(b"HTTP/1.1 200 OK\n")
    client_socket.send(b"Content-Type: text/html\n")
    client_socket.send(b"\n")
    client_socket.sendall(file_content.encode('utf-8'))
    print("HTML-страница отправлена клиенту")
    client_socket.close()