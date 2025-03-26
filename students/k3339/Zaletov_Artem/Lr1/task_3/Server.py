import socket
def start_server(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        while True:
            client_socket, _ = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode()
                print(request)
                if 'GET / HTTP/1.1' in request:
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                    try:
                        with open('index.html', 'r', encoding='utf-8') as f:
                            content = f.read()
                            response += content
                    except FileNotFoundError:
                        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                client_socket.sendall(response.encode())
if __name__ == "__main__":
    start_server()