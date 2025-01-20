import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


input_string = input("Введите три числа (два основания и высоту трапеции), разделённые пробелами: ")


HOST = (socket.gethostname(), 8000)
client_socket.connect(HOST)


client_socket.send(input_string.encode())


response = client_socket.recv(1024)
print(f"Площадь трапеции: {response.decode()}")


client_socket.close()
