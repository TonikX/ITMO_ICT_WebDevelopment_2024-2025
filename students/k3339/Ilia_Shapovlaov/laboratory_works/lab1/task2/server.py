from socket import socket, AF_INET, SOCK_STREAM


def trapezoid_area(a, b, h):
    return 0.5 * (a + b) * h


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(("localhost", 8080))
    server_socket.listen()
    with server_socket.accept()[0] as client_socket:
        data = client_socket.recv(1024).decode()
        ans = trapezoid_area(*[int(x) for x in data.split()])
        client_socket.sendall(str(ans).encode())
