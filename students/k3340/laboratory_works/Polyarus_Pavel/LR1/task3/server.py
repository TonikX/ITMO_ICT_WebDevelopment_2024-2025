import socket

HOST = 'localhost'
PORT = 8080  

HTML_FILE = "index.html" 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}")

while True:
    client_conn, client_addr = server_socket.accept()
    print(f'Подключение от {client_addr}')

    request = client_conn.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    with open(HTML_FILE, 'r') as f:
        body = f.read().encode()

    header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode()
    
    response = client_conn.sendall(header + body)

    client_conn.close()



