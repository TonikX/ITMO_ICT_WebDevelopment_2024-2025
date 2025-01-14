from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import generics
from .models import *
from .serializers import  ProfessionSerializer, WarriorCreateSerializer, WarriorSerializer, SkillSerializer

class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorCreateSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})

class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionSerializer(data=profession)
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
       serializer = SkillSerializer(data=skill)
       if serializer.is_valid(raise_exception=True):
           skill_saved = serializer.save()

       return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})
#ПР2
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