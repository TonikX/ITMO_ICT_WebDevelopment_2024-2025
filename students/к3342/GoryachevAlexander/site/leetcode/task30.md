# 36. Valid Sudoku

Шаги алгоритма:
	1.	Пройдем по каждой строке и проверим уникальность чисел.
	2.	Пройдем по каждому столбцу и проверим уникальность чисел.
	3.	Пройдем по каждому подблоку 3x3 и проверим уникальность чисел.
	4.	Если на любом шаге обнаружится повторение числа, сразу вернем False.
	5.	Если все проверки пройдены успешно, вернем True.
Решение:
```python
def isValidSudoku(board):
    # Используем множества для хранения уже встреченных чисел
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    subboxes = [set() for _ in range(9)]  # 9 подблоков 3x3

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == '.':
                continue  # Пропускаем пустые клетки
            
            # Проверка на повторение в строке
            if num in rows[i]:
                return False
            rows[i].add(num)
            
            # Проверка на повторение в столбце
            if num in cols[j]:
                return False
            cols[j].add(num)
            
            # Проверка на повторение в подблоке 3x3
            subbox_index = (i // 3) * 3 + (j // 3)
            if num in subboxes[subbox_index]:
                return False
            subboxes[subbox_index].add(num)
    
    return True
```