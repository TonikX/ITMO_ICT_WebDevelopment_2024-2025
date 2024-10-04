from socket import socket, AF_INET, SOCK_DGRAM

def server():
   server = socket(AF_INET, SOCK_DGRAM)
   server.bind(('localhost', 2024))

   message, client_port = server.recvfrom(2024)

   print(f'Message from client: {message.decode()}')

   server.sendto(b'Hello, client', client_port)
   server.close()

if __name__ == "__main__":
    task1_server()
