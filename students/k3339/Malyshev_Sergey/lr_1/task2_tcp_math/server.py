import socket

HOST = 'localhost'
PORT = 9090

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print("Server started, waiting for connection...")

    conn, addr = sock.accept()
    print('Connected:', addr)

    data = conn.recv(1024).decode("utf-8").strip()
    print(f"Received: '{data}'")

    parts = data.split()
    if len(parts) != 3:
        response = "Error: exactly 3 numbers required (a b c)"
    else:
        try:
            a = float(parts[0])
            b = float(parts[1])
            c = float(parts[2])

            if a == 0:
                response = "Error: coefficient a cannot be zero"
            else:
                d = b ** 2 - 4 * a * c

                if d > 0:
                    x1 = (-b + d ** 0.5) / (2 * a)
                    x2 = (-b - d ** 0.5) / (2 * a)
                    response = f"Two real roots:\nx1 = {x1:.4f}\nx2 = {x2:.4f}"
                elif d == 0:
                    x = -b / (2 * a)
                    response = f"One real root:\nx = {x:.4f}"
                else:
                    response = f"No real roots\nD = {d:.4f}"

        except ValueError:
            response = "Error: all values must be numbers"

    conn.sendall(response.encode("utf-8"))
    print("Result sent. Closing connection.")

    conn.close()
    sock.close()


if __name__ == "__main__":
    main()