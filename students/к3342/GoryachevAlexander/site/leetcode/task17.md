# 21. Merge Two Sorted Lists
1.	Создаем виртуальную голову нового списка (dummy node), которая упрощает работу с указателями.
2.	Создаем указатель current, который будет указывать на последний узел в новом списке.
3.	Итерируем по двум исходным спискам, сравнивая значения текущих узлов. Добавляем узел с меньшим значением в новый список, сдвигаем указатель.
4.	Когда один из списков закончится, добавляем оставшийся список в конец нового списка, так как он уже отсортирован.
5.	Возвращаем новый список, начиная с первого узла после виртуальной головы.

Решение:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1: ListNode, list2: ListNode) -> ListNode:
    # Создаем виртуальный узел, который будет служить началом нового списка
    dummy = ListNode()
    current = dummy
    
    # Пока оба списка не пусты
    while list1 and list2:
        if list1.val < list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Если один из списков еще не пуст, добавляем оставшиеся элементы
    if list1:
        current.next = list1
    elif list2:
        current.next = list2
    
    # Возвращаем голову нового списка (skip dummy node)
    return dummy.next
```