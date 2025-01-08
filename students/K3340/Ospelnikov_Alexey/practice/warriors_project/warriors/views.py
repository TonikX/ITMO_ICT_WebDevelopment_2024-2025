from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from warriors.models import Warrior
from warriors.serializers import WarriorSerializer


class WarriorAPIView(APIView):
   def get(self, request):
       warriors = Warrior.objects.all()
       serializer = WarriorSerializer(warriors, many=True)
       return Response({"Warriors": serializer.data})

