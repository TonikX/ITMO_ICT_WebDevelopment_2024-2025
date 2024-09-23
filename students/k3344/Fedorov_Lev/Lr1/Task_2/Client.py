import socket

HOST = 'localhost'
PORT = 8091
BUFF_SIZE = 1024


def start_client():
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        a, b, h = map(float, input("Input numbers a b h with whitespace: ").split())

    except ValueError:
        print("Error: might be numbers")
        return

    data = f"{a}, {b}, {h}"

    with socket_client:
        socket_client.connect((HOST, PORT))
        socket_client.sendall((data.encode()))

        response = socket_client.recv(BUFF_SIZE).decode()
        print(f"{response}")


if __name__ == "__main__":
    start_client()
