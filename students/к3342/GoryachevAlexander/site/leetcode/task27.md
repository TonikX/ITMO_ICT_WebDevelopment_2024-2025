# 33. Search in Rotated Sorted Array

Шаги алгоритма:
	1.	Начать с двух указателей: left = 0 и right = len(nums) - 1.
	2.	На каждом шаге вычисляем индекс среднего элемента и сравниваем его с целевым числом.
	3.	В зависимости от того, какая часть массива отсортирована, сужаем поиск.
Решение:
```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # If the left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # If the right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1
```