import socket


def get_input():
    operation = input("Enter operation (pythagorean, quadratic, trapezoid_area, parallelogram_area): ").strip()
    if operation == 'pythagorean':
        a = float(input("Enter side a: "))
        b = float(input("Enter side b: "))
        return f"{operation} {a} {b}"
    elif operation == 'quadratic':
        a = float(input("Enter coefficient a: "))
        b = float(input("Enter coefficient b: "))
        c = float(input("Enter coefficient c: "))
        return f"{operation} {a} {b} {c}"
    elif operation == 'trapezoid_area':
        a = float(input("Enter base1 (a): "))
        b = float(input("Enter base2 (b): "))
        h = float(input("Enter height (h): "))
        return f"{operation} {a} {b} {h}"
    elif operation == 'parallelogram_area':
        base = float(input("Enter base: "))
        height = float(input("Enter height: "))
        return f"{operation} {base} {height}"
    else:
        return "Invalid operation"


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    request = get_input()
    client_socket.sendall(request.encode('utf-8'))
    response = client_socket.recv(1024)
    print(f"Result: {response.decode('utf-8')}")

    client_socket.close()


if __name__ == "__main__":
    start_client()
