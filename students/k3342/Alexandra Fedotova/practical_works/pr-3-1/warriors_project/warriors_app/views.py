from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import *
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, WarriorDetailSerializer, WarriorAndProfessionSerializer, WarriorAndSkillSerializer


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})

class ProfessionCreateView(APIView):
   def post(self, request):
       serializer = ProfessionCreateSerializer(data=request.data)

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
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
            return Response(
                {"Success": f"Skill '{skill_saved.title}' created successfully."}
            )
        return Response(serializer.errors, status=400)


class WarriorListAPIView(ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer

class WarriorCreateView(APIView):
    def post(self, request):
        serializer = WarriorSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            warrior_saved = serializer.save()
            return Response(
                {"Success": f"Warrior '{warrior_saved.name}' created successfully."}
            )
        return Response(serializer.errors, status=400)

class WarriorDeleteView(DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorUpdateView(UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

class WarriorDetailView(RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer


class WarriorAndProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorAndProfessionSerializer(warriors, many=True)
        return Response({"Warriors and Professions": serializer.data})


class WarriorAndSkillsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorAndSkillSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})
