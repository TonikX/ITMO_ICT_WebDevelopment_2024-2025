# [Удаление дубликатов из отсортированного массива](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150)

## Решение

Для решения задачи используется метод двух указателей:
1. Один указатель (`write_index`) отслеживает позицию для записи следующего уникального элемента.
2. Второй указатель (`read_index`) проходит по всем элементам массива, начиная со второго.
3. Если текущий элемент (на позиции `read_index`) не равен предыдущему (на позиции `read_index - 1`), то это уникальный элемент. Он записывается на позицию `write_index`, и указатель `write_index` увеличивается.
4. В конце функция возвращает значение `write_index` как количество уникальных элементов.

### Код решения

```python
from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0

        write_index = 1  # Начинаем с 1, так как первый элемент всегда уникален

        for read_index in range(1, len(nums)):
            if nums[read_index] != nums[read_index - 1]:
                nums[write_index] = nums[read_index]
                write_index += 1

        return write_index
```
