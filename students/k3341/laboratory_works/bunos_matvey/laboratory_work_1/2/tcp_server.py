import socket


def calculate_pythagoras(aa, bb):
    return (aa**2 + bb**2)**0.5


HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server is listening')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = conn.recv(1024).decode()
        a_str, b_str = data.split(',')
        a = float(a_str)
        b = float(b_str)
        c = calculate_pythagoras(a, b)
        conn.sendall(str(c).encode())
