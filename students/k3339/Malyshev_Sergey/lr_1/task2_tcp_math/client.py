import socket

HOST = 'localhost'
PORT = 9090


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print("Connected to server.")
    print("Solving quadratic equation ax² + bx + c = 0")

    user_input = input("Enter coefficients a b c (separated by space): ").strip()

    sock.sendall(user_input.encode("utf-8"))

    response = sock.recv(1024).decode("utf-8")

    print("\nResult from server:")
    print(response)

    sock.close()
    print("Connection closed.")


if __name__ == "__main__":
    main()