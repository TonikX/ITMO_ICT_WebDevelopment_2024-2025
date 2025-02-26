import socket

def read_html():
    with open('index.html', 'r') as file:
        return file.read()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1234))
server.listen(1)

conn, addr = server.accept()
html_content = read_html()

response = f"""HTTP/1.1 200 OK
Content-type: text/html
{html_content}
"""

conn.send(response.encode())
conn.close()