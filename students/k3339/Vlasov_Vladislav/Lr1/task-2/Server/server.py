import socket
import struct

sock = socket.socket()

sock.bind(("127.0.0.1", 14902))

sock.listen(5)

isListen = True
while isListen:
    conn, addr = sock.accept()
    print(f"New connection from {addr[0]}:{addr[1]}")

    try:
        operationType = conn.recv(1).decode("utf-8")
        match operationType:
            case "a":
                a = struct.unpack("d", conn.recv(8))[0]
                b = struct.unpack("d", conn.recv(8))[0]
                print(a, b)
                conn.sendall(struct.pack("d", (a**2 + b**2)**0.5))

            case "b":
                a = struct.unpack("d", conn.recv(8))[0]
                b = struct.unpack("d", conn.recv(8))[0]
                c = struct.unpack("d", conn.recv(8))[0]
                d = b**2 - 4*a*c
                if d > 0:
                    conn.sendall(int(2).to_bytes(1))
                    conn.sendall(struct.pack("d", (-1*b + d**0.5) / (2*a)))
                    conn.sendall(struct.pack("d", (-1*b - d**0.5) / (2*a)))
                elif d == 0:
                    conn.sendall(int(1).to_bytes(1))
                    conn.sendall(struct.pack("d", -1*b / (2*a)))
                else:
                    conn.sendall(int(0).to_bytes(1))
                    conn.sendall(bytes("Решения нет", "utf-8"))

            case "c":
                a = struct.unpack("d", conn.recv(8))[0]
                b = struct.unpack("d", conn.recv(8))[0]
                h = struct.unpack("d", conn.recv(8))[0]
                conn.sendall(struct.pack("d", (a + b)/2 * h))

            case "d":
                a = struct.unpack("d", conn.recv(8))[0]
                h = struct.unpack("d", conn.recv(8))[0]
                conn.sendall(struct.pack("d", a * h))

            case _:
                raise Exception("Invalid first byte")

    except Exception as ex:
        print("Runtime error", ex)
        conn.close()