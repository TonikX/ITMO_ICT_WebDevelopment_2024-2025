from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Warrior
from .serializers import WarriorSerializer

'''
Реализовать ендпоинты:
- Вывод полной информации о всех войнах и их профессиях (в одном запросе).
- Вывод полной информации о всех войнах и их скилах (в одном запросе).
- Вывод полной информации о войне (по id), его профессиях и скилах.
- Удаление война по id.
- Редактирование информации о войне.
'''


class WarriorViewSet(viewsets.ModelViewSet):
    queryset = Warrior.objects.all()
    serializer_class = WarriorSerializer

    @action(detail=False, methods=['get'])
    def professions(self, request):
        warriors = Warrior.objects.select_related('profession').all()
        serializer = self.get_serializer(warriors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def skills(self, request):
        warriors = Warrior.objects.prefetch_related('skill').all()
        serializer = self.get_serializer(warriors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        warrior = self.get_object()
        serializer = self.get_serializer(warrior)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        warrior = self.get_object()
        warrior.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        warrior = self.get_object()
        serializer = self.get_serializer(warrior, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
