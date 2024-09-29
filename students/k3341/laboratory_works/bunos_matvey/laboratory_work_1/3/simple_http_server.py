import socket
import datetime

HOST = '127.0.0.1'
PORT = 8080

with open('index.html', 'r') as file:
    html_content = file.read()

response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

{html_content}"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f'Serving HTTP on port {PORT}')
    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(1024).decode()
            print(request)
            conn.sendall(response.replace('${current_time}', datetime.datetime.now().isoformat()).encode())
            conn.close()
