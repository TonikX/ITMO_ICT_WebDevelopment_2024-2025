import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print("Server started, waiting for connection...")

    while True:
        conn, addr = sock.accept()
        print('Connected:', addr)

        request = conn.recv(1024).decode('utf-8')
        print("Received request:")
        print(request)

        try:
            with open("index.html", "r", encoding="utf-8") as file:
                html_content = file.read()
        except FileNotFoundError:
            html_content = "<h1>file index.html not found</h1>"

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
        conn.sendall(response.encode('utf-8'))

        conn.close()

if __name__ == "__main__":
    main()

