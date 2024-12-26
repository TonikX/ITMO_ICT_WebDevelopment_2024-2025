from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Warrior, Skill, Profession
from .serializers import WarriorSerializer, ProfessionCreateSerializer, SkillSerializer, SkillCreateSerializer, \
    WarriorCreateSerializer, WarriorSkillSerializer, WarriorProfessionSerializer, WarriorDetailSerializer

class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class SkillCreateView(generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillCreateSerializer

class WarriorListAPIView(generics.ListAPIView):
   serializer_class = WarriorSerializer
   queryset = Warrior.objects.all()

class ProfessionCreateAPIView(generics.CreateAPIView):
   serializer_class = ProfessionCreateSerializer
   queryset = Profession.objects.all()

class WarriorCreateAPIView(generics.CreateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorCreateSerializer

class WarriorWithSkillListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSkillSerializer

class WarriorWithProfessionListAPIView(generics.ListAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorProfessionSerializer

class WarriorDetailAPIView(generics.RetrieveAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorDetailSerializer
    lookup_field = 'id'

class WarriorDeleteAPIView(generics.DestroyAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'

class WarriorUpdateAPIView(generics.UpdateAPIView):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer
    lookup_field = 'id'