import socket

server = socket.socket()

host = '127.0.0.1'
port = 1024
server.bind((host, port))

server.listen(5)

while True:
    client, (client_host, client_port) = server.accept()
    client.recv(1000)
    response_type = 'HTTP/1.1 200 OK\n'
    headers = 'Content-Type: text/html\n\n'
    with open('index.html', 'r') as f:
        html_file = f.read()
    body = html_file
    response = response_type + headers + body
    client.send(response.encode('utf-8'))
    client.close()