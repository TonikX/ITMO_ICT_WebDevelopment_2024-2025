import socket

SERVER_ADDR = ("localhost", 9090)

def calculate_trapezoid_area(a, b, h):
    return (a + b) * h / 2

def handle_client(sock, addr):
    data = sock.recv(1024)
    if not data:
        print(f"[*] Client {addr[0]}{addr[1]} disconnected")
        return

    request = data.decode("utf-8").strip()
    print(f"[Message from {addr[0]}:{addr[1]}] {request}")

    try:
        parts = request.split(";")
        if len(parts) != 3:
            raise ValueError("Expected three numbers separated by ';'")

        a = float(parts[0])
        b = float(parts[1])
        h = float(parts[2])

        area = calculate_trapezoid_area(a, b, h)
        response = f"The area of a trapezoid with bases {a}, {b} and height {h} = {area:.4f}"
    except ValueError as e:
        response = f"Error: {e}"

    sock.send(response.encode("utf-8"))

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # чтобы сразу после перезапуска сервера заново привязать его к тому же порту без ошибки
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDR)
    server_socket.listen(socket.SOMAXCONN)

    print(f"[*] TCP-server started on {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Client {client_address[0]}{client_address[1]} connected")

            try:
                handle_client(client_socket, client_address)
            except (ConnectionResetError, BrokenPipeError) as e:
                print(f"[Error] {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("[*] TCP-server stopped")
    finally:
        server_socket.close()

