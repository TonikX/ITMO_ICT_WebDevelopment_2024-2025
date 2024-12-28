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