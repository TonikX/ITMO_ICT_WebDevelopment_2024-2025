import socket


def trapezoid_area(a_side, b_side, h_side):
    return (a_side + b_side)*h_side/2


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 1234))
    server_socket.listen()
    print("Server started")
    client_connection, client_address = server_socket.accept()
    with client_connection:
        client_message = client_connection.recv(1024).decode()
        a, b, h = client_message.split(',')
        client_connection.sendall(str(trapezoid_area(float(a), float(b), float(h))).encode())
        print("Client got the result")