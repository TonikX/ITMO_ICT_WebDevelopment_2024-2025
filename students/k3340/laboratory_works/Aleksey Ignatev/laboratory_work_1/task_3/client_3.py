import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(("localhost", 2003))

        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        client_socket.send(request.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    except Exception as e:
        print("Error:", str(e))
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
