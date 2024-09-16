import socket
import traceback

sock = socket.socket()

sock.bind(("127.0.0.1", 14903))
print("Сервер запущен")

sock.listen(1)

isListen = True
while isListen:
    try:
        conn, addr = sock.accept()
        conn.settimeout(10)
        print(f"Соединение установлено: {addr[0]}:{addr[1]}")
        
        request = b""
        while not b"\r\n\r\n" in request:
            request += conn.recv(1024)

        request = request.decode("utf-8")
        
        if request.startswith("GET"):

            with open("index.html", "r", encoding="utf-8") as file:
                bodyRequest = file.read().encode("utf-8")

            contentLength = len(bodyRequest)

            response = bytes("HTTP/1.0 200 OK\r\n", "utf-8")
            response += bytes(f"Content-Length: {contentLength}\r\n", "utf-8")
            response += bytes("\r\n", "utf-8")
            response += bodyRequest

            conn.sendall(response)

            conn.close()

        elif request.startswith("CLOSE"):
            print("Close Request")
            isListen = False

        else:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            raise Exception("400 Bad Request")

    except Exception:
        print("Соединение разорвано")
        traceback.print_exc()
        conn.close()