import socket

IP = '127.0.0.1'
PORT = 2020

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
headers = b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
try:
  while True:
    client, address = server.accept()
    with open('index.html', 'rb') as f:
      content = f.read()
    client.send(headers + content)
    client.shutdown(socket.SHUT_WR)
except KeyboardInterrupt:
  server.close()