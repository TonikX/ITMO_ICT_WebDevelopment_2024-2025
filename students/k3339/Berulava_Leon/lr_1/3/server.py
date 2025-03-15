import socket

# Чтение содержимого HTML-файла
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Создание HTTP-ответа
response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content)}

{html_content}
"""


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind(('localhost', 8080))


server_socket.listen(1)
print("Server is listening on port 8080...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")


    request = client_socket.recv(1024).decode('utf-8')
    print(f"Request:\n{request}")

    client_socket.sendall(response.encode('utf-8'))

    client_socket.close()
