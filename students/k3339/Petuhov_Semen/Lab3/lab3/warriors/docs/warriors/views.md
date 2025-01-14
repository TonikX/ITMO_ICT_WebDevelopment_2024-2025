# Настраиваем нужные эндпоинты
```python
# 1.Вывод полной информации о всех войнах и их профессиях
class WarriorListView(generics.ListAPIView):
    queryset = Warrior.objects.select_related('profession').all()
    serializer_class = WarriorSerializer

# 2.Вывод полной информации о всех войнах и их скилах
class WarriorSkillsListView(generics.ListAPIView):
    queryset = Warrior.objects.prefetch_related('skill').all()
    serializer_class = WarriorSerializer

# 3.Вывод полной информации о войне (по id), его профессиях и скилах
class WarriorDetailView(generics.RetrieveAPIView):
    queryset = Warrior.objects.select_related('profession').prefetch_related('skill').all()
    serializer_class = WarriorSerializer

# 4.Удаление война по id
class WarriorDeleteView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

# 5.Редактирование информации о войне
class WarriorUpdateView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
```