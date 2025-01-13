from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import Warrior, Skill
from .serializers import (WarriorSerializer, 
                          ProfessionCreateSerializer, 
                          SkillSerializer, 
                          WarriorProfessionSerializer, 
                          WarriorSkillsSerializer, 
                          WarriorCreateSerializer,
                          WarriorDetailSerializer)
from rest_framework import generics

class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})
   
class WarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = WarriorCreateSerializer
   queryset = Warrior.objects.all()
   
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
   
class ProfessionCreateView(APIView):
   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})
   
class WarriorProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.select_related('profession')
    serializer_class = WarriorProfessionSerializer

class WarriorSkillsListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.prefetch_related('skill')
    serializer_class = WarriorSkillsSerializer


class WarriorDetailAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.select_related('profession').prefetch_related('skill')
    serializer_class = WarriorDetailSerializer


class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
