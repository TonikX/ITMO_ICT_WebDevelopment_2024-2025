from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Warrior, Skill 
from .serializers import *

# Create your views here.
class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class SkillListView(APIView):
    """
    Получение списка всех скиллов
    """
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

class SkillCreateView(APIView):
    """
    Создание нового скилла
    """
    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": f"Skill '{skill_saved.title}' created successfully."}, status=status.HTTP_201_CREATED)


class WarriorWithProfessionAPIView(APIView):
    """
    Войн с профессией
    """
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorWithProfessionSerializer(warriors, many=True)
        return Response(serializer.data)


class WarriorWithSkillsAPIView(APIView):
    """
    Войн со скиллом
    """
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorWithSkillsSerializer(warriors, many=True)
        return Response(serializer.data)


class WarriorDetailAPIView(APIView):
    """
    Войн с профессией и скиллом
    """
    def get(self, request, pk):
        warrior = Warrior.objects.prefetch_related('skill').select_related('profession').get(pk=pk)
        serializer = WarriorDetailSerializer(warrior)
        return Response(serializer.data)


class WarriorDeleteAPIView(APIView):
    """
    Удаление война
    """
    def delete(self, request, pk):
        try:
            warrior = Warrior.objects.get(pk=pk)
            warrior.delete()
            return Response({'success': 'Warrior deleted successfully'})
        except Warrior.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)


class WarriorUpdateAPIView(APIView):
    """
    Обновление война
    """
    def put(self, request, pk):
        try:
            warrior = Warrior.objects.get(pk=pk)
        except Warrior.DoesNotExist:
            return Response({'error': 'Warrior not found'}, status=404)
        
        serializer = WarriorUpdateSerializer(warrior, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Warrior updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)
