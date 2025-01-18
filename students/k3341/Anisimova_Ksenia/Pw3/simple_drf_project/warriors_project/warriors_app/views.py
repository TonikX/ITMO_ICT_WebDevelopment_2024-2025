from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView, Response

from .models import Warrior, Skill
from .serializers import WarriorSerializer, SkillSerializer


class SkillsGetView(APIView):
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


class WarriorListWithProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response(serializer.data)


class WarriorListWithSkillsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response(serializer.data)


class WarriorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.prefetch_related('skill').select_related('profession')
    serializer_class = WarriorSerializer

    def delete(self, request, *args, **kwargs):
        warrior = self.get_object()
        warrior.delete()
        return Response({"message": "Warrior deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        warrior = self.get_object()
        serializer = self.serializer_class(warrior, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)