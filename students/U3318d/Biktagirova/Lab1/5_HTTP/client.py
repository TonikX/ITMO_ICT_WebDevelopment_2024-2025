import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 8080
BUFF_SIZE = 2048

client_socket.connect((HOST, PORT))


def _post(subject='web', grade=4):
        try:
            query_string = f"name={subject.lower()}&grade={grade}"
            client_request = (
                f"POST /subjects?{query_string} HTTP/1.1\r\n"
                f"Host: {HOST}\r\n\r\n"
                #f"\n\n\n"
            )
            client_socket.send(client_request.encode('iso-8859-1'))
            server_response = client_socket.recv(BUFF_SIZE).decode('iso-8859-1')
            client_socket.close()
            print(server_response)
        except Exception as e:
            print(f"Error: {e}")



def _get(subject='web'):
    try:
        headers = (
            f"GET /users/{subject.lower()} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n\r\n"
        )
        client_socket.sendall(headers.encode('iso-8859-1'))
        server_response = client_socket.recv(BUFF_SIZE).decode('iso-8859-1')
        print(server_response)
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__=='__main__':
    opt = input("post or get: ")
    match opt:
        case 'post':
            sub = input("enter the subject: ")
            gr = int(input("enter the grade: "))
            _post(sub, gr)
        case 'get':
            sub = input("enter the subject: ")
            _get(sub)


#POST /subjects?name=maths&grade=5 HTTP/1.1
