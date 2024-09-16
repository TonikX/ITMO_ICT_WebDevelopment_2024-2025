import socket
import threading

def startClient():

    global isClientWork

    conn = socket.socket()
    conn.connect(("127.0.0.1", 14904))

    connectProof = conn.recv(1)
    if not int().from_bytes(connectProof, byteorder="big") == 1:
        conn.close()
        isClientWork = False
        return
    
    listenThread = threading.Thread(target=listenResponse, args=(conn,), daemon=True)
    listenThread.start()

    while isClientWork:
        message = input()

        request = message.encode("utf-8")
        
        requestPieces = [request[i : i + MAX_LEN] for i in range(0, len(request), MAX_LEN)]

        for piece in requestPieces:
            conn.sendall(len(piece).to_bytes(2, byteorder="big"))
            conn.sendall(piece)

def listenResponse(conn: socket.socket):

    global isClientWork

    try:
        while isClientWork:
            response = conn.recv(2)

            if not response:
                isClientWork = False
                print("Сервер разорвал соединение")
                break

            messageLen = int().from_bytes(response, byteorder="big")

            response = b""
            while len(response) < messageLen:
                tmpData = conn.recv(min(1024, messageLen - len(response)))
                response += tmpData

            print(response.decode("utf-8"))

    except:
        isClientWork = False
        print("Ошибка, разрыв соединения ...")
        conn.close()


if __name__ == "__main__":
    
    MAX_LEN = 2**16 - 1
    isClientWork = True
    startClient()

    print("Соединение разорвано")