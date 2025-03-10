# 8. String to Integer (atoi)
Алгоритм решения задачи:
	1.	Игнорируем все начальные пробелы.
	2.	Определяем знак числа (если это “-” или “+”).
	3.	Читаем цифры, игнорируя остальные символы.
	4.	Преобразуем строку в число, с учетом знака.
	5.	Проверяем, находится ли число в пределах 32-битного диапазона. Если нет, обрезаем его.
```python
def myAtoi(s: str) -> int:
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    
    # Убираем начальные пробелы
    s = s.lstrip()
    
    # Если строка пустая, сразу возвращаем 0
    if not s:
        return 0
    
    # Определяем знак
    sign = 1
    if s[0] == '-':
        sign = -1
        s = s[1:]
    elif s[0] == '+':
        s = s[1:]
    
    # Читаем цифры
    result = 0
    for char in s:
        if not char.isdigit():
            break
        result = result * 10 + int(char)
    
    # Применяем знак
    result *= sign
    
    # Проверка на выход за диапазон
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    
    return result
```