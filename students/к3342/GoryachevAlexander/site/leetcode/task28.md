# 34. Find First and Last Position of Element in Sorted Array

Шаги алгоритма:
	1.	Поиск первой позиции: Начнём с бинарного поиска, чтобы найти первое вхождение target. Если находим target, продолжаем искать в левой части, пока не встретим его первый раз.
	2.	Поиск последней позиции: Аналогично, начинаем бинарный поиск, но теперь после нахождения элемента будем продолжать искать в правой части, чтобы найти последнее вхождение.
Решение:
```python
def searchRange(nums, target):
    def findFirstPosition(nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                if mid == 0 or nums[mid - 1] != target:
                    return mid
                right = mid - 1
        return -1
    
    def findLastPosition(nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                if mid == len(nums) - 1 or nums[mid + 1] != target:
                    return mid
                left = mid + 1
        return -1

    first = findFirstPosition(nums, target)
    if first == -1:
        return [-1, -1]
    
    last = findLastPosition(nums, target)
    return [first, last]
```