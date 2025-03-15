from .serializers import *
from rest_framework.views import APIView, Response
from rest_framework import generics

# class WarriorAPIView(APIView):
#     def get(self, request):
#         warriors = Warrior.objects.all()
#         serializer = WarriorListSerializer(warriors, many=True)
#         return Response({'warriors': serializer.data})

class ProfessionAPICreate(APIView):
   def post(self, request):
       profession = request.data.get("profession")
       serializer = ProfessionCreateSerializer(data=profession)

       if serializer.is_valid(raise_exception=True):
           profession_saved = serializer.save()

       return Response({"success": "Profession '{}' created succesfully.".format(profession_saved.title)})
   
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
    
class WarriorListAPIView(generics.ListAPIView):
    serializer_class = WarriorListSerializer
    queryset = Warrior.objects.all()

class WarriorAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WarriorListSerializer
    queryset = Warrior.objects.all()
