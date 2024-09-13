import socket

buffer_size = 1024
host = 'localhost'
port = 8000
path = '/Users/bellesbae/itmo/ITMO_ICT_WebDevelopment_2024-2025/students/k3342/Senichev_Sergey/Lr1/task3/'
server_address = (host, port)

def load_html_file():
    try:
        with open(path + 'index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>Файл index.html не найден!</h1>"

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)  # waiting for 5 clients simultaneously

    print(f"Server is running on {host}:{port}")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Client connection: {client_address}")

        request = client_connection.recv(buffer_size).decode('utf-8')
        print(f"Client request:\n{request}")

        response_body = load_html_file()

        http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + response_body
        )

        client_connection.sendall(http_response.encode())
        client_connection.close()

if __name__ == "__main__":
    server()
