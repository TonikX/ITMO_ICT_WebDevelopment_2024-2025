from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from warriors_app import models, serializers


class WarriorAPIView(APIView):
    def get(self, request):
        warriors = models.Warrior.objects.all()
        serializer = serializers.WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = serializers.ProfessionSerializer(data=profession)

        serializer.is_valid(raise_exception=True)
        profession_saved = serializer.save()

        return Response(data={"Success": f"Profession {profession_saved.title!r} created successfully."})
    

class SkillView(APIView):
    def get(self, request):
        skills = models.Skill.objects.all()
        serializer = serializers.SkillSerializer(skills, many=True)
        return Response(data={"skills": serializer.data})

    def post(self, request):
        skill = request.data.get("skill")
        serializer = serializers.SkillSerializer(data=skill)

        serializer.is_valid(raise_exception=True)
        saved_skill = serializer.save()

        return Response(data={"Success": f"skill {saved_skill.title!r} created successfully."})
    

class WarriorListAPIView(generics.ListAPIView):
   serializer_class = serializers.WarriorSerializer
   queryset = models.Warrior.objects.all()


class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = serializers.ProfessionSerializer
   queryset = models.Profession.objects.all()


class WarriorWithProfessionView(generics.ListAPIView):
    serializer_class = serializers.WarriorWithProfessionSerializer
    queryset = models.Warrior.objects.select_related("profession").all()


class WarriorWithSkillView(generics.ListAPIView):
    serializer_class = serializers.WarriorWithSkillSerializer
    queryset = models.Warrior.objects.prefetch_related("skill").all()


class WarriorDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.WarriorDetailSerializer
    queryset = models.Warrior.objects.select_related("profession").prefetch_related("skill")


class WarriorDeleteView(generics.DestroyAPIView):
    queryset = models.Warrior.objects.all()
    serializer_class = serializers.WarriorSerializer
    lookup_field = "pk"


class WarriorUpdateView(generics.UpdateAPIView):
    queryset = models.Warrior.objects.all()
    serializer_class = serializers.WarriorDetailSerializer
    lookup_field = "pk"
