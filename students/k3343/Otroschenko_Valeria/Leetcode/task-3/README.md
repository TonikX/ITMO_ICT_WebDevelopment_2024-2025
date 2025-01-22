# Merge k Sorted Lists
## Level: Hard
## Description

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

### Example 1:

Input:
```
lists = [[1,4,5],[1,3,4],[2,6]]
```
Output:
```
[1,1,2,3,4,4,5,6]
```
Explanation:
The linked-lists are:
```
[
  1->4->5,
  1->3->4,
  2->6
]
```
Merging them into one sorted list:
```
1->1->2->3->4->4->5->6
```

### Example 2:

Input:
```
lists = []
```
Output:
```
[]
```

### Example 3:

Input:
```
lists = [[]]
```
Output:
```
[]
```

### Constraints:

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.

## Solution

Реализовано решение задачи с использованием **минимальной кучи (heap)** для эффективного слияния списков с временной сложностью \(O(N \log k)\), где \(N\) — общее количество узлов, а \(k\) — количество списков.

#### Основные шаги:

1. **Инициализация кучи**:
   - Добавляем в кучу первые узлы всех непустых списков. Каждый элемент кучи представляет собой кортеж `(значение узла, индекс списка, узел)`.

2. **Слияние**:
   - Постепенно извлекаем минимальный элемент из кучи и добавляем его в результирующий связанный список.
   - Если у извлеченного узла есть следующий узел, добавляем его в кучу.

3. **Возврат результата**:
   - После обработки всех узлов возвращаем результирующий связанный список.

#### Примеры:

- **Пример 1:**
  ```
  Input: lists = [[1,4,5],[1,3,4],[2,6]]
  Output: [1,1,2,3,4,4,5,6]
  ```

- **Пример 2:**
  ```
  Input: lists = []
  Output: []
  ```

- **Пример 3:**
  ```
  Input: lists = [[]]
  Output: []
  ```

#### Примечания:

- Решение использует кучу для эффективной обработки минимального элемента из всех списков, поддерживая временную сложность \(O(N \log k)\).

## Result
![Result](task-3-result.jpg)
