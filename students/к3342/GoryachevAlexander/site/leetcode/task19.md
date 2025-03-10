# 24. Swap Nodes in Pairs
1.	Нам нужно пройти по связанному списку и каждую пару соседних узлов менять местами.
2.	Для этого мы будем использовать три указателя:
•	prev — указывает на предыдущий узел.
•	first — указывает на первый узел пары, которую нужно поменять местами.
•	second — указывает на второй узел пары.
3.	Для каждой пары:
•	Меняем ссылки first и second.
•	Соединяем prev с новым первым узлом пары.
•	Перемещаем указатели вперед на следующую пару.
4.	Мы продолжаем процесс до конца списка, когда у нас не останется пар.

Решение:
```python
# Определение структуры узла связанного списка
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def swapPairs(head: ListNode) -> ListNode:
    # Создаем фиктивную голову для упрощения работы с головой списка
    dummy = ListNode(-1)
    dummy.next = head
    
    prev = dummy  # Инициализируем prev как фиктивную голову
    
    while head and head.next:
        # Указываем на первую и вторую пару узлов
        first = head
        second = head.next
        
        # Выполняем обмен
        prev.next = second
        first.next = second.next
        second.next = first
        
        # Перемещаем указатели
        prev = first
        head = first.next
    
    return dummy.next  # Возвращаем новый head списка
```