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









