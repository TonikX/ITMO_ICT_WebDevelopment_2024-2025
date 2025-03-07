from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Warrior, Skill
from .serializers import WarriorSerializer, SkillSerializer, ProfessionCreateSerializer, SkillCreateSerializer, \
    WarriorWithProfessionSerializer, WarriorWithSkillsSerializer, WarriorWithSkillsAndProfessionSerializer


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
        return Response({"Success": f"Profession '{profession_saved.title}' created successfully."})


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
        return Response({"Success": f"Profession '{skill_saved.title}' created successfully."})


class WarriorListWithProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response(serializer.data)


class WarriorWithProfessionListView(generics.ListAPIView):
    serializer_class = WarriorWithProfessionSerializer
    queryset = Warrior.objects.all()


class WarriorWithSkillsListView(generics.ListAPIView):
    serializer_class = WarriorWithSkillsSerializer
    queryset = Warrior.objects.all()


class WarriorDetailView(generics.RetrieveAPIView):
    serializer_class = WarriorWithSkillsAndProfessionSerializer
    queryset = Warrior.objects.all()
    lookup_field = 'id'


class WarriorDeleteView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
