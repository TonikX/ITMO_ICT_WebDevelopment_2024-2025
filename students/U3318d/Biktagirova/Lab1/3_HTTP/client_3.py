import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 8080
BUFF_SIZE = 2048

client_socket.connect((HOST, PORT))
client_request = f"GET / HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
client_socket.send(client_request.encode())

server_response = client_socket.recv(BUFF_SIZE)
print(server_response.decode())

client_socket.close()
