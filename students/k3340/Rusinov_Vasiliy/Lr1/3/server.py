import socket

def load_html_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def create_http_response(content):
    response = f"HTTP/1.1 200 OK\r\n"
    response += f"Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += f"\r\n"
    response += content
    return response

def start_server(host='127.0.0.1', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started at http://{host}:{port}")

    while True:
        client_connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        request = client_connection.recv(1024).decode()
        print(f"Request:\n{request}")

        if request:
            html_content = load_html_file('index.html')
            http_response = create_http_response(html_content)
            client_connection.sendall(http_response.encode())

        client_connection.close()

if __name__ == "__main__":
    start_server()
