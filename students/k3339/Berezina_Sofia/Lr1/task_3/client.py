import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('127.0.0.1', 1024))

http_request = 'GET / HTTP/1.1\r\nHost: localhost:555\r\n\r\n'

conn.send(http_request.encode('utf-8'))

print(conn.recv(1000).decode('utf-8'))
conn.close()