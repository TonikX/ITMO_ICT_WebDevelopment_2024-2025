import socket
import threading
import traceback

from typing import List, Any

def startServer():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 14904))
    sock.listen()

    listenThread = threading.Thread(target=listenConnects, args=(sock,), daemon=True)
    listenThread.start()

    sendThread = threading.Thread(target=sendMessage, daemon=True)
    sendThread.start()

def listenConnects(sock: socket.socket):
    while isServerWork:
        conn, addr = sock.accept()

        clientThread = threading.Thread(target=listenClients, args=(conn, addr), daemon=True)
        clientThread.start()

def listenClients(conn: socket.socket, addr: List[Any]):

    print(f"Установка соединения с клиентом {addr[0]}:{addr[1]} ...")

    global clientsList
    clientsList.append((addr, conn))

    conn.sendall(int(1).to_bytes(1, byteorder="big"))

    print(f"Установка соединения с клиентом {addr[0]}:{addr[1]} ЗАВЕРШЕНА")

    try:
        isClienstConnect = True
        while isClienstConnect:
            request = conn.recv(2)

            if not request:
                closeConnect(conn, addr)
                isClienstConnect = False
                break

            messageLen = int().from_bytes(request, byteorder="big")

            request = b""
            while len(request) < messageLen:
                tmpData = conn.recv(min(1024, messageLen - len(request)))
                request += tmpData

            global messagesQueue
            messagesQueue.append((addr, request.decode("utf-8")))

    except:
        closeConnect(conn, addr)

def closeConnect(conn: socket.socket, addr: List[any]):
    print(f"Разрыв соединения с клиентом {addr[0]}:{addr[1]} ...")

    global clientsList
    try:
        clientsList.remove((addr, conn))
    except Exception:
        traceback.print_exc()

    try:
        conn.close()
    except:
        pass
    
    print(f"Разрыв соединения с клиентом {addr[0]}:{addr[1]} ЗАВЕРШЕН")

def sendMessage():
    
    while isServerWork:
        for messageBlock in messagesQueue:
            addr, message = messageBlock

            #print(f"Отправитель: {addr[0]}:{addr[1]}")
            #print(f"Сообщение: {message}")

            responseString = f"Отправитель: {addr[0]}:{addr[1]}\nСообщение: {message}"
            response = responseString.encode("utf-8")   

            responsePieces = [response[i : i + MAX_LEN] for i in range(0, len(response), MAX_LEN)]

            for addr, conn in clientsList:
                try:
                    for piece in responsePieces:
                        conn.sendall(len(piece).to_bytes(2, byteorder="big"))
                        conn.sendall(piece)
                except Exception:
                    print(f"Ошибка при отправке сообщения клиенту {addr[0]}:{addr[1]}")
                    traceback.print_exc()
                    closeConnect(conn, addr)

            messagesQueue.remove(messageBlock)

"""
    except Exception:
        print("Критическая ошибка во время отправки сообщения")
        traceback.print_exc()
"""

if __name__ == "__main__":

    messagesQueue: List[tuple[List[Any], str]] = []
    clientsList: List[tuple[List[Any], socket.socket]] = []
    isServerWork = True
    MAX_LEN = 2**16 - 1

    startServer()

    while isServerWork:
        if input() == "exit":
            isServerWork = False