from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from warriors.models import Warrior, Skill
from warriors.serializers import (
    WarriorSerializer,
    ProfessionSerializer,
    SkillSerializer,
)


class WarriorListView(generics.ListCreateAPIView):
    # def get(self, request):
    #     warriors = Warrior.objects.all()
    #     serializer = WarriorSerializer(warriors, many=True)
    #     return Response({"Warriors": serializer.data})
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response(
            {"Success": f"Profession '{profession_saved.title}' created succesfully."}
        )


class SkillListView(APIView):
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
        return Response(
            {"Success": f"Skill '{skill_saved.title}' created succesfully."}
        )
