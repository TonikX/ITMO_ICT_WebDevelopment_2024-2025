from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from yaml import serialize

from .serializers import *

class WarriorAPIView(generics.RetrieveAPIView):
    serializer_class = WarriorSerializer
    lookup_field = 'id'
    def get_queryset(self):
        queryset = Warrior.objects.filter(pk=self.kwargs['id'])
        return queryset


class WarriorDeleteAPIView(generics.DestroyAPIView):
    serializer_class = WarriorSerializer
    lookup_field = 'id'
    def get_queryset(self):
        queryset = Warrior.objects.filter(pk=self.kwargs['id'])
        return queryset

class WarriorUpdateAPIView(generics.UpdateAPIView):
    serializer_class = WarriorSerializer
    lookup_field = 'id'
    queryset = Warrior.objects.all()


class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorCreateView(generics.CreateAPIView):
    serializer_class = WarriorCreateSerializer


class ProfessionCreateView(generics.CreateAPIView):
    serializer_class = ProfessionCreateSerializer


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillsSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(skill_saved.title)})
