import socket


def send_and_receive_message():
    client_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 2003)
    msg_to_server = "Hello, server!"

    try:
        client_s.sendto(msg_to_server.encode('utf-8'), server_address)
        response_from_server, _ = client_s.recvfrom(1234)
        print("Response from server:", response_from_server.decode("utf-8"))
    except Exception as e:
        print("Error:", str(e))
    finally:
        client_s.close()


if __name__ == "__main__":
    send_and_receive_message()
