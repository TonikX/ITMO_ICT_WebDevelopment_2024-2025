# Longest Palindromic Substring
Алгоритм решения задачи:
	1.	Проходим по всем возможным подстрокам строки.
	2.	Для каждой подстроки проверяем, является ли она палиндромом.
	3.	Возвращаем самую длинную палиндромную подстроку.
Решение:
```python
def longestPalindrome(s: str) -> str:
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]
    
    longest = ""
    for i in range(len(s)):
        odd_palindrome = expand_around_center(i, i)
        even_palindrome = expand_around_center(i, i+1)
        longest = max(longest, odd_palindrome, even_palindrome, key=len)
    
    return longest
```