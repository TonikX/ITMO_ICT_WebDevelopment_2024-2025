import socket

html_file = open('index.html')
html_data = '\n'.join(html_file.readlines())
response_type = "HTTP/1.1 200 OK"
content_type = "Content-Type: text/html"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 14900))
server.listen(1)

client_socket, client_address = server.accept()
answer = f"{response_type}\n{content_type}\n\n{html_data}"
client_socket.send(bytes(answer, 'UTF-8'))
client_socket.close()
server.close()