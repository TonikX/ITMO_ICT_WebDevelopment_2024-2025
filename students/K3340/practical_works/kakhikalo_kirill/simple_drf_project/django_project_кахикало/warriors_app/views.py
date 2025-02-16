from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from warriors_app.models import Warrior, Skill
from warriors_app.serializers import WarriorSerializer, ProfessionSerializer, SkillSerializer, WarriorDetailSerializer

class ProfessionCreateView(APIView):

   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    """
    GET endpoint to list all skills.
    """

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    """
    POST endpoint to create a new skill.
    """

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response({"Success": f"Skill '{skill_saved.title}' created successfully."})

class WarriorListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer

class WarriorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer

class WarriorCreateView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer