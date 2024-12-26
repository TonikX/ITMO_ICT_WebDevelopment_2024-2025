# [Удаление всех вхождений элемента из массива](https://leetcode.com/problems/remove-element/?envType=study-plan-v2&envId=top-interview-150)

## Решение

Для решения задачи используется метод двух указателей:
1. **`write_index`** указывает на позицию, куда нужно записать следующий элемент, не равный `val`.
2. **`read_index`** проходит по всем элементам массива.
3. Если текущий элемент `nums[read_index]` не равен `val`, он записывается на позицию `write_index`, и `write_index` увеличивается.

### Код решения

```python
from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        write_index = 0  # Указатель для записи элементов

        for read_index in range(len(nums)):
            if nums[read_index] != val:
                nums[write_index] = nums[read_index]
                write_index += 1

        return write_index
```
