from rest_framework import generics
from .models import Warrior, Skill, Profession, SkillOfWarrior
from .serializers import WarriorSerializer, ProfessionSerializer, SkillSerializer, SkillOfWarriorSerializer

class WarriorCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового воина
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class WarriorListAPIView(generics.ListAPIView):
    """
    Представление для получения всех воинов
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()


class ProfessionCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания новой профессии
    """
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()


class ProfessionListAPIView(generics.ListAPIView):
    """
    Представление для получения всех профессий
    """
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()


class SkillListAPIView(generics.ListAPIView):
    """
    Представление для получения всех умений
    """
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового умения
    """
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillOfWarriorListAPIView(generics.ListAPIView):
    """
    Представление для получения всех умений
    """
    serializer_class = SkillOfWarriorSerializer
    queryset = SkillOfWarrior.objects.all()


class SkillOfWarriorCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового умения
    """
    serializer_class = SkillOfWarriorSerializer
    queryset = SkillOfWarrior.objects.all()


class WarriorWithProfessionListAPIView(generics.ListAPIView):
    """
    Вывод полной информации о всех воинах и их профессиях
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.select_related('profession').all()


class WarriorWithSkillsListAPIView(generics.ListAPIView):
    """
    Вывод полной информации о всех воинах и их скилах
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.prefetch_related('skillofwarrior_set__skill').all()


class WarriorDetailAPIView(generics.RetrieveAPIView):
    """
    Вывод полной информации о воине (по id), его профессиях и скилах
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()


class WarriorDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление воина по id
    """
    queryset = Warrior.objects.all()


class WarriorUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование информации о воине
    """
    serializer_class = WarriorSerializer
    queryset = Warrior.objects.all()
