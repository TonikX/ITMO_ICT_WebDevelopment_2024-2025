from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class WarriorProfessionListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorSkillsListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSkillSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillSerializer(data=skill)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({
                            "Success": "Skill '{}' created succesfully.".format(
                                skill_saved.title)})


class WarriorDetailAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'


class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'


class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorRowSerializer
    lookup_field = 'id'