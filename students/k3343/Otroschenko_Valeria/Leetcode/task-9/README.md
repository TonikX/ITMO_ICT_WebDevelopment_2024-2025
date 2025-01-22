# N-Queens Puzzle
## Level: Hard

## Description

The N-Queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return all distinct solutions to the N-Queens puzzle. Each solution contains a distinct board configuration of the N-Queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.

### Example 1:

Input:
```
n = 4
```
Output:
```
[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
```
Explanation:
There exist two distinct solutions to the 4-queens puzzle as shown below:

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
[["Q"]]
```

### Constraints:

- `1 <= n <= 9`

## Solution

Решение использует **обратное отслеживание (backtracking)** для генерации всех возможных конфигураций доски, которые удовлетворяют правилам.

### Основные шаги:

1. **Инициализация:**
   - Используются множества `cols`, `diagonals`, и `anti_diagonals` для отслеживания занятых столбцов, диагоналей и анти-диагоналей.
   - Доска представлена как список списков с символами `'.'`.

2. **Функция обратного отслеживания:**
   - Для каждой строки перебираются все столбцы.
   - Проверяется возможность размещения ферзя в текущей клетке.
   - Если размещение валидное, ферзь устанавливается, и функция вызывается для следующей строки.
   - После обработки строки ферзь убирается, чтобы вернуться к предыдущему состоянию.

3. **Сохранение результатов:**
   - Если все строки обработаны, текущая конфигурация доски добавляется в список решений.

### Примечания:
- Алгоритм имеет временную сложность \(O(n!)\), так как с каждым ферзем количество доступных позиций уменьшается.
- Используется \(O(n^2)\) дополнительной памяти для хранения доски и вспомогательных структур.

## Result
![Result](task-9-result.jpg)