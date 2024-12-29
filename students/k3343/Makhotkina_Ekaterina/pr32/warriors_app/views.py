from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Skill, Warrior, SkillOfWarrior
from .serializers import WarriorProfessionSerializer, ProfessionSerializer, WarriorSkillsSerializer, WarriorSerializer, \
    WarriorFullSerializer, \
    SkillSerializer, WarriorFullInfoSerializer, WarriorWithSkillsSerializer, WarriorWithProfessionSerializer


class WarriorsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorFullSerializer
    lookup_field = 'id'


class WarriorProfessionAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorCreateView(APIView):
    def post(self, request):
        data = request.data
        serializer = WarriorSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            warrior_saved = serializer.save()
            return Response({"Success": f"Warrior '{warrior_saved.name}' created successfully."}, status=201)
        else:
            return Response({"Error": "Invalid data provided"}, status=400)


class WarriorSkillsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSkillsSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


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

        return Response({"Success": "Skill '{}' created successfully.".format(skill_saved.title)})


class WarriorDeleteView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'


class WarriorUpdateView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'


class WarriorsFullInfoAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related(
            Prefetch('skill', queryset=Skill.objects.all()),
            Prefetch('skillofwarrior_set', queryset=SkillOfWarrior.objects.select_related('skill')),
        ).select_related('profession')

        serializer = WarriorFullInfoSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorsWithSkillsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related(
            Prefetch('skill', queryset=Skill.objects.all())
        )
        serializer = WarriorWithSkillsSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorsWithProfessionsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession')
        serializer = WarriorWithProfessionSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})
