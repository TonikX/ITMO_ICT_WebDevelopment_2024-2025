import socket

SERVER_ADDR = ("localhost", 9090)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    a = float(input("a = "))
    b = float(input("b = "))
    h = float(input("h = "))

    request = f"{a};{b};{h}"

    client_socket.settimeout(5.0)

    try:
        client_socket.connect(SERVER_ADDR)
        client_socket.send(request.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print(f"[Message from {SERVER_ADDR[0]}:{SERVER_ADDR[1]}] {response}")
    except ConnectionRefusedError:
        print("[Error] Server is not available")
    except socket.timeout:
        print("[Error] Server timeout")
    finally:
        client_socket.close()
