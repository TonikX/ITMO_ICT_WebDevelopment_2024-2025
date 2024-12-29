# Практическая работа №3.2

## Задание

Цель работы: получить представление об использовании возмжностей работы контроллеров и серриализаторов в Django Rest Framework.

Необходимо выполнить все задания с пометкой **"Практическое задание** [из практической работы №3.2] (https://docs.google.com/document/d/1PkpwxCUYQ2_Pi8Fpcgno6te3oCQHZfkh03Zxt6DhHSw/edit?usp=sharing). 

Полученную программу залить в папку этого репозитория **sutdents/группа/practical_works/фамилия_имя/simple_drf_project**. 

Инструкция о загрузке работы ниже. Не забывайте о файле gitignore.

## Code

settings.py:
```python
INSTALLED_APPS = [
  ...
  'rest_framework',
  'warriors_app',
]
```

models.py:
```python
from django.db import models

class Warrior(models.Model):
  """
  Описание война
  """
  race_types = (
    ('s', 'student'),
    ('d', 'developer'),
    ('t', 'teamlead'),
  )
  race = models.CharField(max_length=1, choices=race_types, verbose_name='Расса')
  name = models.CharField(max_length=120, verbose_name='Имя')
  level = models.IntegerField(verbose_name='Уровень', default=0)
  skill = models.ManyToManyField('Skill', verbose_name='Умения', through='SkillOfWarrior',
                                related_name='warrior_skils')
  profession = models.ForeignKey('Profession', on_delete=models.CASCADE, verbose_name='Профессия',
                                blank=True, null=True)

class Profession(models.Model):
  """
  Описание профессии
  """
  title = models.CharField(max_length=120, verbose_name='Название')
  description = models.TextField(verbose_name='Описание')

class Skill(models.Model):
  """
  Описание умений
  """
  title = models.CharField(max_length=120, verbose_name='Наименование')
  def __str__(self):
    return self.title

class SkillOfWarrior(models.Model):
  """
  Описание умений война
  """
  skill = models.ForeignKey('Skill', verbose_name='Умение', on_delete=models.CASCADE)
  warrior = models.ForeignKey('Warrior', verbose_name='Воин', on_delete=models.CASCADE)
  level = models.IntegerField(verbose_name='Уровень освоения умения')
```

serializers.py:
```python
from rest_framework import serializers
from .models import *

class WarriorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Warrior
    fields = "__all__"

class ProfessionCreateSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=120)
  description = serializers.CharField()

  def create(self, validated_data):
    profession = Profession(**validated_data)
    profession.save()
    return Profession(**validated_data)

class SkillSerializer(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = "__all__"

class SkillCreateSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=120)

  def create(self, validated_data):
    skill = Skill(**validated_data)
    skill.save()
    return Skill(**validated_data)

class ProfessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profession
    fields = "__all__"

class SkillOfWarriorSerializer(serializers.ModelSerializer):
  skill = SkillSerializer()
  class Meta:
    model = SkillOfWarrior
    fields = "__all__"

class WarriorSkillSerializer(serializers.ModelSerializer):
  skill = SkillOfWarriorSerializer(many=True, source='skillofwarrior_set')
  class Meta:
    model = Warrior
    fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
  profession = ProfessionSerializer()
  class Meta:
    model = Warrior
    fields = "__all__"

class WarriorSkillProfessionSerializer(serializers.ModelSerializer):
  skill = SkillOfWarriorSerializer(many=True, source='skillofwarrior_set')
  profession = ProfessionSerializer()
  class Meta:
    model = Warrior
    fields = "__all__"
```

urls.py:
```python
from django.urls import path
from .views import *

app_name = "warriors_app"

urlpatterns = [
  path('warriors/', WarriorAPIView.as_view()),
  path('profession/create/', ProfessionCreateView.as_view()),
  path('skills/', SkillAPIView.as_view()),
  path('skill/create/', SkillCreateView.as_view()),
  path('warrior/<int:pk>/', WarriorDetailView.as_view()),
  path('warriors-skills/', WarriorSkillListView.as_view()),
  path('warriors-professions/', WarriorProfessionListView.as_view()),
  path('warriors-full/<int:pk>/', WarriorProfessionListView.as_view()),
]
```

views.py:
```python
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import Warrior, Skill
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, SkillCreateSerializer, WarriorSkillSerializer, WarriorProfessionSerializer, WarriorSkillProfessionSerializer

class WarriorAPIView(APIView):
  def get(self, request):
    warriors = Warrior.objects.all()
    serializer = WarriorSerializer(warriors, many=True)
    return Response({"Warriors": serializer.data})

class ProfessionCreateView(APIView):
  def post(self, request):
    profession = request.data.get("profession")
    serializer = ProfessionCreateSerializer(data=profession)
    if serializer.is_valid(raise_exception=True):
      profession_saved = serializer.save()
    return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})

class SkillAPIView(APIView):
  def get(self, request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response({"Skills": serializer.data})

class SkillCreateView(APIView):
  def post(self, request):
    skill = request.data.get("skill")
    serializer = SkillCreateSerializer(data=skill)
    if serializer.is_valid(raise_exception=True):
      skill_saved = serializer.save()
    return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})

class WarriorListView(generics.ListAPIView):
  queryset = Warrior.objects.all()
  serializer_class = WarriorSerializer

class WarriorSkillListView(generics.ListAPIView):
  queryset = Warrior.objects.all()
  serializer_class = WarriorSkillSerializer

class WarriorProfessionListView(generics.ListAPIView):
  queryset = Warrior.objects.all()
  serializer_class = WarriorProfessionSerializer

class WarriorDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Warrior.objects.all()
  serializer_class = WarriorSerializer

class WarriorDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Warrior.objects.all()
  serializer_class = WarriorSkillProfessionSerializer
```