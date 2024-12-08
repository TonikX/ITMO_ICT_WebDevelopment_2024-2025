from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorCreateView(APIView):
    def post(self, request):
        warrior = request.data.get("warrior")
        serializer = WarriorCreateSerializer(data=warrior)
        if serializer.is_valid(raise_exception=True):
            warrior_saved = serializer.save()
        return Response({"Success": "Warrior '{}' created succesfully.".format(warrior_saved.name)})


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionCreateSerializer(data=profession)
        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()
        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillAPIView(APIView):
    def get(self, request):
        skill = Skill.objects.all()
        serializer = SkillSerializer(skill, many=True)
        return Response({"Skills": serializer.data})


class SkillCreateView(APIView):
    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"Success": "Skill '{}' created succesfully.".format(skill_saved.title)})


class SkillOfWarriorCreateView(APIView):
    def post(self, request):
        skill_of_warrior = request.data.get("skill_of_warrior")
        serializer = SkillOfWarriorSerializer(data=skill_of_warrior)
        if serializer.is_valid(raise_exception=True):
            skill_of_warrior_saved = serializer.save()
        return Response({"Success": "Skill '{}' created succesfully.".format(skill_of_warrior_saved.skill)})


class WarriorWithProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorWithProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorWithSkillAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorWithSkillSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorDetailAPIView(APIView):
    def get(self, request, pk):
        warrior = Warrior.objects.prefetch_related('skill').select_related('profession').get(id=pk)
        serializer = WarriorSerializer(warrior)
        return Response({"Warrior": serializer.data})


class WarriorDeleteView(DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer


class WarriorUpdateView(UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

    def get(self, request, *args, **kwargs):
        warrior = self.get_object()
        serializer = self.get_serializer(warrior)
        return Response(serializer.data)
