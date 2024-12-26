import socket

host = 'localhost'
port = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((host, port))

request = f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
client_socket.send(request.encode())

response = client_socket.recv(4096)
print("Полученный ответ от сервера:")
print(response.decode())

client_socket.close()
