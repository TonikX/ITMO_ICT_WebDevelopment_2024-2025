import socket

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_client.sendto("Hello, server".encode(), ("127.0.0.1", 9090))
response, server_address = udp_client.recvfrom(1024)
print(f"Message: {response.decode()}")
