import socket
def main():
    host = '127.0.0.1'
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096).decode()
        print("Ответ сервера:\n", response)
if __name__ == "__main__":
    main()