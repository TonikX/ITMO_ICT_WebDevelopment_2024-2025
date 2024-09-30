import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
client.sendall(http_request.encode('utf-8'))

response = client.recv(4096)
print(response.decode('utf-8'))
client.close()