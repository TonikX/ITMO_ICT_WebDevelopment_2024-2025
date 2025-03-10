# 28. Find the Index of the First Occurrence in a String
1.	Используем встроенный метод find(), который доступен для строк в Python.
2.	Метод find() возвращает индекс первого вхождения подстроки в строку или -1, если подстрока не найдена.
Решение:
```python
def strStr(haystack, needle):
    return haystack.find(needle)
```