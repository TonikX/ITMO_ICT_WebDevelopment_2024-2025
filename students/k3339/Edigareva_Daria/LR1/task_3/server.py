import socket

def load_html(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")

    request = client_socket.recv(1024).decode('utf-8')
    print(f"Запрос от клиента:\n{request}")

    html_content = load_html('index.html')

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html_content)}\r\n\r\n{html_content}"

    client_socket.sendall(response.encode('utf-8'))

    client_socket.close()
