from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Warrior, Skill, Profession
from .serializers import WarriorSerializer, ProfessionSerializer, SkillSerializer, WarriorWithSkillsSerializer, \
    WarriorDetailSerializer, WarriorWithProfessionSerializer


class WarriorAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorCreateAPIView(generics.CreateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class ProfessionCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()


class SkillCreateAPIView(generics.CreateAPIView):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillListAPIView(generics.ListAPIView):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class WarriorWithProfessionListView(generics.ListAPIView):
    serializer_class = WarriorWithProfessionSerializer
    queryset = Warrior.objects.select_related('profession').all()


class WarriorWithSkillsListView(generics.ListAPIView):
    serializer_class = WarriorWithSkillsSerializer
    queryset = Warrior.objects.prefetch_related('skill').all()


class WarriorDetailAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorDetailSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skill').all()


class WarriorDeleteAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()



