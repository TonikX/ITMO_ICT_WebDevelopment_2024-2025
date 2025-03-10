# 35. Search Insert Position

Шаги алгоритма:
	1.	Устанавливаем два указателя: left на начало массива и right на конец массива.
	2.	Пока left <= right:
	•	Находим середину массива mid = (left + right) // 2.
	•	Если nums[mid] == target, возвращаем индекс mid.
	•	Если nums[mid] < target, сдвигаем левый указатель вправо, т.е. left = mid + 1.
	•	Если nums[mid] > target, сдвигаем правый указатель влево, т.е. right = mid - 1.
	3.	Если мы не нашли элемент, то по завершению бинарного поиска, указатель left будет указывать на индекс, куда можно вставить target.
Решение:
```python
def searchInsert(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return left
```