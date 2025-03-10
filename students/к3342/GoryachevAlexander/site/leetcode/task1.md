# Find missing and repeating values
Для решения задачи:
	1.	Пройдем по всем числам в матрице и посчитаем их сумму.
	2.	Используя формулу суммы чисел от 1 до n², вычислим, какой номер отсутствует.
	3.	Найдем число, которое повторяется.
	4.	Вернем массив, содержащий повторяющееся и отсутствующее число.

Решение:
```python
def find_duplicate_and_missing(grid):
    n = len(grid)
    total_sum = 0
    expected_sum = (n * n * (n * n + 1)) // 2
    seen = set()

    for row in grid:
        for num in row:
            total_sum += num
            if num in seen:
                repeat = num
            seen.add(num)
    
    missing = expected_sum - (total_sum - repeat)
    
    return [repeat, missing]
```