import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 2003))

    try:
        operation = input(
            "Choose operation (1 - Pythagorean theorem, 2 - Trapezoid area, 3 - Parallelogram area): ")

        if operation not in ["1", "2", "3"]:
            print("Wrong operation code")
            return

        params = input("Enter the operation parameters (separated by commas):")

        client_socket.send(f"{operation},{params}".encode('utf-8'))

        result = client_socket.recv(1024).decode('utf-8')

        print("Result:", result)

    except Exception as e:
        print("Error:", str(e))
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
