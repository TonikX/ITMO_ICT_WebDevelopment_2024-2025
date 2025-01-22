# Distinct Subsequences
## Level: Hard

## Description

Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.

The test cases are generated so that the answer fits on a 32-bit signed integer.

### Example 1:

Input:
```
s = "rabbbit", t = "rabbit"
```
Output:
```
3
```
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from `s`:
```
rabbbit
rabbbit
rabbbit
```

### Example 2:

Input:
```
s = "babgbag", t = "bag"
```
Output:
```
5
```
Explanation:
As shown below, there are 5 ways you can generate "bag" from `s`:
```
babgbag
babgbag
babgbag
babgbag
babgbag
```

### Constraints:

- `1 <= s.length, t.length <= 1000`
- `s` and `t` consist of English letters.

## Solution

Решение использует **динамическое программирование (DP)** для подсчёта количества различных подпоследовательностей.

### Основные шаги:

1. **Инициализация таблицы DP:**
   - `dp[i][j]` обозначает количество различных способов составить первые `j` символов строки `t` из первых `i` символов строки `s`.
   - Базовый случай: Любая строка может сформировать пустую строку `t` единственным способом, удалив все символы. Поэтому `dp[i][0] = 1`.

2. **Заполнение таблицы DP:**
   - Если текущие символы `s[i-1]` и `t[j-1]` совпадают:
     ```
     dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
     ```
     Первый компонент учитывает использование текущего символа, второй — его пропуск.
   - Если символы не совпадают:
     ```
     dp[i][j] = dp[i-1][j]
     ```

3. **Результат:**
   - Значение в `dp[m][n]` даёт количество способов сформировать строку `t` из строки `s`.

### Примечания:
- Алгоритм имеет временную сложность \(O(m \times n)\), где \(m\) и \(n\) — длины строк `s` и `t` соответственно.
- Используется \(O(m \times n)\) памяти для хранения таблицы DP.

## Result
![Result](task-15-result.jpg)
