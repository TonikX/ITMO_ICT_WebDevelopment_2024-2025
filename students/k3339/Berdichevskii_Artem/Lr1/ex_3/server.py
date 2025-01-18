import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        with open('index.html', 'rb') as f:
            html_content = f.read()

        http_header = f'''HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

'''.encode('utf-8')

        conn.sendall(http_header + html_content)