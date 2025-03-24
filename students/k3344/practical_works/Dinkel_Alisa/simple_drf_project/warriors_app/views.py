from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Warrior, Skill
from .serializers import WarriorSerializer, SkillSerializer, WarriorDetailSerializer, WarriorWithProfessionSerializer,\
    WarriorWithSkillsSerializer


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class SkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarriorsWithProfessionsView(generics.ListAPIView):
    queryset = Warrior.objects.select_related("profession").all()
    serializer_class = WarriorWithProfessionSerializer


class WarriorsWithSkillsView(generics.ListAPIView):
    queryset = Warrior.objects.prefetch_related("skill").all()
    serializer_class = WarriorWithSkillsSerializer


class WarriorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer
