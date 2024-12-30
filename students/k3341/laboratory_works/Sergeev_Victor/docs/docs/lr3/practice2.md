# Практическая работа 2

Для выполнения работы было создано django веб-приложение warriors. Приложение содержит модели:

* Warrior - модель война
    * race: varchar(1) - раса война
    * name: varchar(120) - имя война
    * level: integer - уровень война
    * skill: many_to_many(Skill, throught=SkillOfWarrior) - способности война

* Profession - модель профессии
    * title: varchar(120) - название профессии
    * description: text - описание профессии

* Skill - модель способности
    * title: varchar(120) - название способности

* SkillOfWarrior - модель способности война
    * skill: foreign_key(Skill) - способность
    * warrior: foreign_key(Warrior) - воин
    * level: integer - уровень способности

## Задание 1

Реализовать ендпоинты для добавления и просмотра скилов методом, описанным в пункте выше.

serializers.py

```python
from rest_framework import serializers
from .models import *

class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
```

views.py

```python
from .serializers import *
from rest_framework.views import APIView, Response

class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillListSerializer(skills, many=True)
        return Response({"skills": serializer.data})

class SkillAPICreate(APIView):
    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"success": "Skill '{}' created succesfully".format(skill_saved.title)})
```

urls.py

```python
from django.urls import path
from .views import *

app_name = 'warrior_app'

urlpatterns = [
    path('skill/', SkillAPIView.as_view()),
    path('skill/create/', SkillAPICreate.as_view()),
]
```

## Задание 2

Реализовать ендпоинты:

* Вывод полной информации о всех войнах и их профессиях (в одном запросе).
* Вывод полной информации о всех войнах и их скилах (в одном запросе).
* Вывод полной информации о войне (по id), его профессиях и скилах.
* Удаление война по id.
* Редактирование информации о войне.

serializers.py

```python
from rest_framework import serializers
from .models import *

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "title", "description"]

class SkillOfWarriorSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='skill.title')
    id = serializers.IntegerField(source='skill.id')

    class Meta:
        model = SkillOfWarrior
        fields = ['id', 'title', 'level']

class WarriorListSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(many=False)
    skill = SkillOfWarriorSerializer(source='skillofwarrior_set', many=True)

    class Meta:
        model = Warrior
        fields = ["id", "race", "name", "level", "skill", "profession"]
```

views.py

```python
class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorListSerializer
    queryset = Warrior.objects.all()

class WarriorAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WarriorListSerializer
    queryset = Warrior.objects.all()
```

urls.py

```python
from django.urls import path
from .views import *

app_name = 'warrior_app'

urlpatterns = [
    path('skill/', SkillAPIView.as_view()),
    path('skill/create/', SkillAPICreate.as_view()),
    path('warrior/', WarriorListAPIView.as_view()),
    path('warrior/<int:pk>/', WarriorAPIView.as_view()),
]
```
