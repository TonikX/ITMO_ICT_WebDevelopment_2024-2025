import socket

def main():
    conn = socket.socket()

    conn.connect(("127.0.0.1", 14903))

    request = b"GET\r\n\r\n"

    #request = b"CLOSE\r\n\r\n"

    conn.send(request)

    tmpData = conn.recv(512)

    if not tmpData:
        print("Not data")
        return

    response = b""
    response += tmpData
    while not b"\r\n\r\n" in response:
        tmpData = conn.recv(512)
        response += tmpData

    responseString = response.decode("utf-8")

    responseCode = responseString.split("\r\n")[0].split(" ")[1]

    try:
        if int(responseCode) != 200:
            print(f"Плохой код ответа: {int(responseCode)}")
            return
    except Exception:
        print("Неккоректный ответ сервера", responseCode)
        return

    headers = {}
    for head in responseString.split("\r\n")[1:]:
        if not head:
            break
        key, value = head.split(":")
        headers[f"{key.strip()}"] = int(value.strip())

    takedBodyLenght = len(response.split(sep=b"\r\n\r\n")[1])
    responseBoby = conn.recv(headers["Content-Length"] - takedBodyLenght)

    body = response.split(sep=b"\r\n\r\n")[1]
    body = body.decode("utf-8") + responseBoby.decode("utf-8")

    print(body)
    conn.close()
    return

if __name__ == "__main__":
    main()