import socket

def read_html_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

def create_http_response(html_content):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n"
        "\r\n"
        "{}"
    ).format(len(html_content), html_content)
    return response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1234))
s.listen(1)

while True:
    client_socket, client_address = s.accept()
    with client_socket:
        print(f"Подключен клиент: {client_address}")

        html_content = read_html_file('index.html')
        http_response = create_http_response(html_content)
        client_socket.sendall(http_response.encode('utf-8'))


