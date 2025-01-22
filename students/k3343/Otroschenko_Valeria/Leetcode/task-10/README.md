# N-Queens Puzzle - Count Solutions
## Level: Hard

## Description

The N-Queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return the number of distinct solutions to the N-Queens puzzle.

### Example 1:

Input:
```
n = 4
```
Output:
```
2
```
Explanation:
There are two distinct solutions to the 4-queens puzzle as shown:

```
.Q..    ..Q.
...Q    Q...
Q...    ...Q
..Q.    .Q..
```

### Example 2:

Input:
```
n = 1
```
Output:
```
1
```

### Constraints:

- `1 <= n <= 9`

## Solution

Решение использует **обратное отслеживание (backtracking)** для подсчёта всех возможных конфигураций, соответствующих правилам.

### Основные шаги:

1. **Инициализация:**
   - Используются множества `cols`, `diagonals`, и `anti_diagonals` для отслеживания занятых столбцов, диагоналей и антидиагоналей.

2. **Рекурсивная функция:**
   - Для каждой строки перебираются все столбцы.
   - Проверяется возможность размещения ферзя в текущей клетке.
   - Если размещение валидное, ферзь устанавливается, и функция вызывается для следующей строки.
   - После обработки строки ферзь убирается, чтобы вернуться к предыдущему состоянию.
   - Если все строки обработаны, счётчик решений увеличивается.

3. **Возврат результата:**
   - После завершения рекурсии возвращается общее количество решений.

### Примечания:
- Алгоритм имеет временную сложность \(O(n!)\), так как с каждым ферзем количество доступных позиций уменьшается.
- Используется \(O(n)\) дополнительной памяти для отслеживания занятых позиций.

## Result
![Result](task-10-result.jpg)
