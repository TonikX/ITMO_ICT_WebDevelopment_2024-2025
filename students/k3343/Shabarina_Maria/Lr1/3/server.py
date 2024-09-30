import socket


with open('index.html', 'r') as file:
    html_content = file.read()

response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

{html_content}"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen()
    print("Server started")
    while True:
        connection, address = server_socket.accept()
        with connection:
            print(connection.recv(1024).decode())
            connection.sendall(response.encode())
            connection.close()