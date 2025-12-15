from __future__ import annotations
import json, math, socket, threading

HOST = "127.0.0.1"
PORT = 5000

def handle_client(conn: socket.socket, addr) -> None:
    with conn:
        f = conn.makefile("rwb", buffering=0)
        print(f"Client connected: {addr}")
        try:
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    payload = json.loads(line.decode("utf-8"))
                    op = payload.get("op")
                    params = payload.get("params", {})

                    if op == "pythagoras":
                        a = float(params["a"]); b = float(params["b"])
                        result = math.hypot(a, b)

                    elif op == "quadratic":
                        A = float(params["a"]); B = float(params["b"]); C = float(params["c"])
                        if A == 0:
                            raise ValueError("Coefficient 'a' must be non-zero for a quadratic.")
                        D = B*B - 4*A*C
                        if D >= 0:
                            sqrtD = math.sqrt(D)
                            x1 = (-B + sqrtD) / (A*2)
                            x2 = (-B - sqrtD) / (A*2)
                            result = {"x1": x1, "x2": x2, "discriminant": D}
                        else:
                            sqrtD = math.sqrt(-D)
                            real = -B / (2*A)
                            imag = sqrtD / (2*A)
                            result = {"x1": f"{real}+{imag}i", "x2": f"{real}-{imag}i", "discriminant": D}

                    elif op == "trapezoid_area":
                        a = float(params["a"]); b = float(params["b"]); h = float(params["h"])
                        result = (a + b) * 0.5 * h

                    elif op == "parallelogram_area":
                        base = float(params["base"]); height = float(params["height"])
                        result = base * height

                    else:
                        raise ValueError(f"Unknown op: {op}")

                    out = {"ok": True, "result": result}
                except Exception as e:
                    out = {"ok": False, "error": str(e)}
                f.write((json.dumps(out) + "\n").encode("utf-8"))
        finally:
            print(f"Client disconnected: {addr}")

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"TCP Math server listening on {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
