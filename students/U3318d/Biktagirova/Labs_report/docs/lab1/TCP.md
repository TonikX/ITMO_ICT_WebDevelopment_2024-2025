## Задание 2:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

- Теорема Пифагора.
- Решение квадратного уравнения.
- Поиск площади трапеции.
- Поиск площади параллелограмма.

### Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

`Server's code`

``` py
import socket
import math
import time

# TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(20)

HOST = 'localhost'
PORT = 8880
BUFF_SIZE = 8

# указываем и порт на котором ожидаем клиентов
server_socket.bind((HOST, PORT))

# OC может отклонять новые подключения(больше 1) или просто их игнорировать
server_socket.listen(1)

print("TCP server is running on", HOST, ':', PORT)

ASK_A = "enter the first side "
ASK_B = "enter the second side "
ASK_a = "enter a"
ASK_b = "enter b"
ASK_c = "enter c"
ASK_base_a = "Enter the base"
ASK_base_b = "Enter the second base"
ASK_h = "Enter the height"
HELLO_1 = "Let's check Pythagoras theorem\n"
HELLO_2 = "Let's solve quadratic equation\n"
HELLO_3 = "Let's find area of trapezoid\n"
HELLO_4 = "Let's find area of parallelogram\n"
HELLO_5 = "Bye!"


while True:
    try:
        start_time = time.perf_counter()
        try:
            # блокирующая строка
            client_conn, address = server_socket.accept()
            print('Connection from: ', address)
        except TimeoutError:
            end_time = time.perf_counter()
            t = '{:.0f}'.format(end_time - start_time)
            print(f'Server stopped: No connections for {t} seconds')
            server_socket.close()
            break

        try:
            while True:
                opt = client_conn.recv(2).decode()
                match int(opt):
                    case 1:
                        client_conn.send(HELLO_1.encode())
                        client_conn.send(ASK_A.encode())
                        a = client_conn.recv(BUFF_SIZE).decode()
                        print("Client's answer: ", a)

                        client_conn.send(ASK_B.encode())
                        b = client_conn.recv(BUFF_SIZE).decode()
                        print("Client's answer: ", b)

                        HYP = round(math.sqrt(int(a) ** 2 + int(b) ** 2), 2)
                        client_conn.send((str(HYP)).encode())
                        print("Sent result: ", HYP)
                    case 2:
                        client_conn.send((HELLO_2 + ASK_a).encode())
                        a = client_conn.recv(2).decode()
                        print("Client's answer: ", a)

                        client_conn.send(ASK_b.encode())
                        b = client_conn.recv(2).decode()
                        print("Client's answer: ", b)

                        client_conn.send(ASK_c.encode())
                        c = client_conn.recv(2).decode()
                        print("Client's answer: ", c)

                        try:
                            ANS1 = round((-1 * int(b) + math.sqrt(int(b)**2 - 4*int(a)*int(c)))/(2*int(a)), 2)
                            ANS2 = round((-1 * int(b) - math.sqrt(int(b) ** 2 - 4 * int(a) * int(c))) / (2 * int(a)),2)
                            client_conn.send(f'x1 = {ANS1} x2 = {ANS2}'.encode())
                            print("Sent result: ", f'x1 = {ANS1} x2 = {ANS2}')
                        except ValueError:
                            client_conn.send("Answer is complex number, sorry I can't solve that".encode())
                            print("Sent result: Answer is complex number, sorry I can't solve that")
                    case 3:
                        client_conn.send(HELLO_3.encode())
                        client_conn.send(ASK_base_a.encode())
                        a = client_conn.recv(2).decode()
                        print("Client's answer: ", a)

                        client_conn.send(ASK_base_b.encode())
                        b = client_conn.recv(2).decode()
                        print("Client's answer: ", b)

                        client_conn.send(ASK_h.encode())
                        h = client_conn.recv(2).decode()
                        print("Client's answer: ", h)

                        ANS1 = round((int(a)+int(b))/2 * int(h),2)
                        client_conn.send(f'Area = {ANS1}'.encode())
                        print("Sent result: ", ANS1)
                    case 4:
                        client_conn.send(HELLO_4.encode())
                        client_conn.send(ASK_base_a.encode())
                        b = client_conn.recv(BUFF_SIZE).decode()
                        print("Client's answer: ", b)

                        client_conn.send(ASK_h.encode())
                        h = client_conn.recv(BUFF_SIZE).decode()
                        print("Client's answer: ", h)

                        AREA = round(int(b)*int(h), 2)
                        client_conn.send((str(AREA)).encode())
                        print("Sent result: ", AREA)
                    case 5:
                        client_conn.send(HELLO_5.encode())
                        print("Sent result: ", HELLO_5)
        except ValueError:
            print("Incorrect data from a client")
        except ConnectionResetError:
            print(f'Client {address} has disconnected')

    except ValueError:
        print("Incorrect data from a client")
        break

    except KeyboardInterrupt:
        server_socket.close()
        break

```
`Client's code`

``` py
import socket
import time


def menu():
    print("Choose one option\n"
          "1 - Pythagoras theorem\n"
          "2 - Quadratic equation\n"
          "3 - Find the area of a trapezoid\n"
          "4 - Find the area of a parallelogram\n"
          "5 - Exit")
    try:
        option = int(input(">> "))
        if option not in [1, 2, 3, 4, 5]:
            print("You've entered wrong value")
        else:
            return option
    except ValueError:
        print("You've entered wrong value")
    except KeyboardInterrupt:
        print("You've stopped client")
        exit()


def pythagoras(cl_sock, mes_size):
        try:
            print("Server's response: ", cl_sock.recv(mes_size).decode())
            cl_mess = int(input())
            cl_sock.send((str(cl_mess)).encode())

            serv_mess = cl_sock.recv(mes_size)
            print("Server's response: ", serv_mess.decode())

            cl_mess = int(input())
            cl_sock.send((str(cl_mess)).encode())

            serv_mess = cl_sock.recv(mes_size)
            print("Server's response: ", serv_mess.decode())

        except KeyboardInterrupt:
            cl_sock.close()
        except ValueError:
            print("You've entered wrong value")


def quadratic(cl_sock, mes_size):
    try:
        print("Server's response: ", cl_sock.recv(mes_size).decode())
        cl_mess = int(input())
        if cl_mess == 0:
            while cl_mess == 0:
                print("a coefficient can't be zero, try again")
                cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

    except KeyboardInterrupt:
        cl_sock.close()
    except ValueError:
        print("You've entered wrong value")


def trapezoid(cl_sock, mes_size):
    try:
        print("Server's response: ", cl_sock.recv(mes_size).decode())
        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

    except KeyboardInterrupt:
        cl_sock.close()
    except ValueError:
        print("You've entered wrong value")


def parallelogram(cl_sock, mes_size):
    try:
        print("Server's response: ", cl_sock.recv(mes_size).decode())
        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

        cl_mess = int(input())
        cl_sock.send((str(cl_mess)).encode())

        serv_mess = cl_sock.recv(mes_size)
        print("Server's response: ", serv_mess.decode())

    except KeyboardInterrupt:
        cl_sock.close()
    except ValueError:
        print("You've entered wrong value")


if __name__ == "__main__":

    HOST = 'localhost'
    PORT = 8880
    BUFF_SIZE = 1024

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        client_socket = None
        print(f"Sorry, connection to {HOST}:{PORT} is refused")
        exit()

    while True:
        opt = menu()
        client_socket.send((str(opt)).encode())
        match opt:
            case 1:
                pythagoras(client_socket, BUFF_SIZE)
            case 2:
                quadratic(client_socket, BUFF_SIZE)
            case 3:
                trapezoid(client_socket, BUFF_SIZE)
                pass
            case 4:
                parallelogram(client_socket, BUFF_SIZE)
                pass
            case 5:
                if(client_socket != None):
                    client_socket.close()
                    exit()
                else:
                    exit()
```
