import socket

server_host = 'localhost'
server_port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
client_socket.sendall(http_request.encode())

response = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    response += data

client_socket.close()

http_response = response.decode('utf-8')
print("Ответ сервера:")
print(http_response)

html_start = http_response.find("\r\n\r\n") + 4
html_content = http_response[html_start:]

client_socket.close()
