from __future__ import annotations
import json, socket

HOST = "127.0.0.1"
PORT = 5000

def send_request(sock: socket.socket, payload: dict) -> dict:
    sock.sendall((json.dumps(payload) + "\n").encode("utf-8"))
    buf = b""
    while True:
        ch = sock.recv(1)
        if not ch:
            raise ConnectionError("Server closed connection")
        if ch == b"\n":
            break
        buf += ch
    return json.loads(buf.decode("utf-8"))

def main() -> None:
    print("Choose operation:")
    print("1) Pythagoras (legs a, b -> hypotenuse)")
    print("2) Quadratic equation (a, b, c)")
    print("3) Trapezoid area (a, b, h)")
    print("4) Parallelogram area (base, height)")
    choice = input("Enter 1-4: ").strip()

    if choice == "1":
        a = float(input("a = ")); b = float(input("b = "))
        payload = {"op": "pythagoras", "params": {"a": a, "b": b}}
    elif choice == "2":
        A = float(input("a = ")); B = float(input("b = ")); C = float(input("c = "))
        payload = {"op": "quadratic", "params": {"a": A, "b": B, "c": C}}
    elif choice == "3":
        a = float(input("a = ")); b = float(input("b = ")); h = float(input("h = "))
        payload = {"op": "trapezoid_area", "params": {"a": a, "b": b, "h": h}}
    elif choice == "4":
        base = float(input("base = ")); height = float(input("height = "))
        payload = {"op": "parallelogram_area", "params": {"base": base, "height": height}}
    else:
        print("Invalid choice."); return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        res = send_request(sock, payload)
        print("Response:", res)

if __name__ == "__main__":
    main()
