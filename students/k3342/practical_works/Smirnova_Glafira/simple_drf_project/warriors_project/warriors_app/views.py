from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Warrior, Skill
from .serializers import (
    ProfessionSerializer,
    SkillSerializer,
    WarriorSerializer,
    WarriorWithProfessionSerializer,
    WarriorWithSkillSerializer,
)


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorWithProfessionView(generics.ListAPIView):
    serializer_class = WarriorWithProfessionSerializer
    queryset = Warrior.objects.select_related("profession").all()


class WarriorWithSkillView(generics.ListAPIView):
    serializer_class = WarriorWithSkillSerializer
    queryset = Warrior.objects.prefetch_related("skill").all()


class WarriorDetailView(RetrieveUpdateDestroyAPIView):
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


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        serializer.is_valid(raise_exception=True)
        profession_saved = serializer.save()

        return Response(
            data={
                "Success": f"Profession '{profession_saved.title}' created succesfully."
            }
        )


class SkillView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(data={"skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = SkillSerializer(data=skill)

        serializer.is_valid(raise_exception=True)
        saved_skill = serializer.save()

        return Response(
            data={
                "Success": f"skill '{saved_skill.title}' created succesfully.",
            }
        )
