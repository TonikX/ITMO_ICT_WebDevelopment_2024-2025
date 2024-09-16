import socket
import struct

OptionsString = """Выберите желаемую операцию: 
a. Теорема Пифагора
b. Решение квадратного уравнения.
c. Поиск площади трапеции.
d. Поиск площади параллелограмма.
exit. Выйти из программы
Ввод: """

def OperationTypeValidate(type: str) -> bool:
    if type not in ["a", "b", "c", "d", "exit"]:
        print("Допустимые символы только \"a\", \"b\", \"c\", \"d\" для выбора операции или \"exit\" для выхода из программы.")
        return False
    
    return True

def OperationDataValidate(data: str, type: str) -> bool:
    if data == "back":
        return True
    
    elif type in ["a", "d"]:
        if len(data.split(" ")) != 2:
            print("Недопустимое количество чисел")
            return False
    
    elif type in ["b", "c"]:
        if len(data.split(" ")) != 3:
            print("Недопустимое количество чисел")
            return False

    for num in data.split(" "):
        try:
            if float(num) > 65535:
                print("Числа должны быть не больше 65535")
                return False
        except:
            print("Получены не числа!")
            return False
            
    return True
    

if __name__ == "__main__":

    
    isWork = True
    while isWork:

        conn = socket.socket()
        conn.connect(("127.0.0.1", 14902))

        while True:
            operationType = input(OptionsString).strip()
            if OperationTypeValidate(operationType):
                break
        
        while True:
            match operationType:
                case "a":
                    print("ВНИМАНИЕ! Допускаются только числа не больше 65535")
                    print("Выбранная операция: Теорема Пифагора.\nДля возврата к выбору введите \"back\"")
                    operationData = input("Введите 2 числа (длины катетов) через пробел: ").strip()
                case "b":
                    print("Выбранная операция: Решение квадратного уравнения.\nДля возврата к выбору введите \"back\"")
                    operationData = input("Введите 3 числа (параметры a, b и c уравнения) через пробел: ").strip()
                case "c":
                    print("Выбранная операция: Поиск площади трапеции.\nДля возврата к выбору введите \"back\"")
                    operationData = input("Введите 3 числа (длины оснований a, b и высоту h) через пробел: ").strip()
                case "d":
                    print("Выбранная операция: Поиск площади параллелограмма.\nДля возврата к выбору введите \"back\"")
                    operationData = input("Введите 2 числа (длину основания и высоту) через пробел: ").strip()
                case "exit":
                    isWork = False
                    #conn.close()
                    break

            if OperationDataValidate(operationData, operationType):
                break
        
        if operationData == "back":
            continue
        
        conn.sendall(operationType.encode("utf-8"))
        for num in operationData.split(" "):
            conn.sendall(struct.pack("d", float(num)))
        
        match operationType:
            case "a":
                x = conn.recv(8)
                print(f"Результат: {struct.unpack("d", x)[0]}")

            case "b":
                solutionsNum = conn.recv(1)
                match int().from_bytes(solutionsNum):
                    case 2:
                        x1 = conn.recv(8)
                        x2 = conn.recv(8)
                        print(f"Результат: x1 = {struct.unpack("d", x1)[0]}, x2 = {struct.unpack("d", x2)[0]}")
                    case 1:
                        x = conn.recv(8)
                        print(f"Результат: x = {struct.unpack("d", x)[0]}")
                    case 0:
                        solutionsNum = conn.recv(1024)
                        print(f"Результат: {solutionsNum.decode("utf-8")}")
            
            case "c":
                S = conn.recv(8)
                print(f"Результат: S = {struct.unpack("d", S)[0]}")

            case "d":
                S = conn.recv(8)
                print(f"Результат: S = {struct.unpack("d", S)[0]}")

        conn.close()