import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    print(f"To calculate the area of the trapezium input")
    a = float(input("Base a: "))
    b = float(input("Base b: "))
    h = float(input("Height h: "))

    message = f"{a},{b},{h}"
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

except Exception as e:
    print(f"Error while communicating with the server: {e}")

finally:
    client_socket.close()