import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)


server_socket.listen(1)
print("Server is waiting for a client...")

while True:

    client_socket, client_address = server_socket.accept()
    print(f"Connected client with the address: {client_address}")

    try:

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Message from client: {data}")

        a, b, h = map(float, data.split(','))

        result = (a+b)/2 * h

        response_message = f"Area of the trapezium: {result}"
        client_socket.send(response_message.encode('utf-8'))

    except Exception as e:
        print(f"Error while calculating the response: {e}")

    finally:
        client_socket.close()