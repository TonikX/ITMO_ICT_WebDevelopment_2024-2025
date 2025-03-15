import socket

HOST = '127.0.0.1'
PORT = 16000
index_path = 'students/k3341/laboratory_works/Sergeev_Victor/lr1/task3/index.html'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    try:
        client, _ = server.accept()
        data = open(index_path).read()
        responce =  'HTTP/1.1 200 OK\r\n' + \
                    'Connection: close\r\n' + \
                    'Content-type: text/html; charset=utf-8;\r\n' + \
                    f'Content-Length: {len(data)}\r\n\r\n' + data
                    
        client.sendall(responce.encode())
        print(f'Server sent:\n {data}')
        client.close()
    except KeyboardInterrupt:
        print('Shutting server...')
        break
    
server.close()
    
