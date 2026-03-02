import socket
import webbrowser
import tempfile

HOST = 'localhost'
PORT = 9090


with socket.socket() as client_socket:
    client_socket.connect((HOST, PORT))

    http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
    client_socket.sendall(http_request.encode('utf-8'))

    response = b""
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    header_end = response.find(b"\r\n\r\n")
    html_content = response[header_end + 4:].decode('utf-8')

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_file_path = f.name

    webbrowser.open(f'file://{temp_file_path}')

    print(response.decode('utf-8'))
