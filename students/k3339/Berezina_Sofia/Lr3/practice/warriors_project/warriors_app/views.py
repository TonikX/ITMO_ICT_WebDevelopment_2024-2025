from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import Warrior, Skill


# Create your views here.
class WarriorAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


# Эндпоинты для умений (скилов)
class SkillAPIView(APIView):
    # GET - просмотр всех скилов
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

    # POST - добавление нового скила
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 1. Вывод всех воинов с их профессиями
class WarriorProfessionListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = WarriorProfessionSerializer(warriors, many=True)
        return Response({
            "count": warriors.count(),
            "warriors": serializer.data
        })


# 2. Вывод всех воинов с их скилами
class WarriorSkillsListAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = WarriorSkillsSerializer(warriors, many=True)
        return Response({
            "count": warriors.count(),
            "warriors": serializer.data
        })


# 3. Вывод полной информации о воине по ID
class WarriorDetailAPIView(APIView):
    def get(self, request, pk):
        warrior = get_object_or_404(Warrior.objects.prefetch_related('skill'), pk=pk)
        serializer = WarriorFullSerializer(warrior)
        return Response(serializer.data)


# 4. Удаление воина по ID
class WarriorDeleteAPIView(APIView):
    def delete(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        warrior_name = warrior.name
        warrior.delete()
        return Response(
            {"message": f"Воин {warrior_name} успешно удален"},
            status=status.HTTP_204_NO_CONTENT
        )


# 5. Редактирование информации о воине
class WarriorUpdateAPIView(APIView):
    def get(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorFullSerializer(warrior)
        return Response(serializer.data)

    def put(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorUpdateSerializer(warrior, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные
            updated_warrior = Warrior.objects.get(pk=pk)
            full_serializer = WarriorFullSerializer(updated_warrior)
            return Response({
                "message": "Информация о воине успешно обновлена",
                "warrior": full_serializer.data
            })

        return Response(
            {"error": "Ошибка валидации", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        warrior = get_object_or_404(Warrior, pk=pk)
        serializer = WarriorUpdateSerializer(warrior, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные
            updated_warrior = Warrior.objects.get(pk=pk)
            full_serializer = WarriorFullSerializer(updated_warrior)
            return Response({
                "message": "Информация о воине успешно обновлена",
                "warrior": full_serializer.data
            })

        return Response(
            {"error": "Ошибка валидации", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )