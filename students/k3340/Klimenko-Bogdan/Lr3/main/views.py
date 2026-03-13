from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

from .models import (
    Habitat, Department, Building, Enclosure, Staff, Animal,
    FeedingRationType, FeedingRation, Zoo, WinteringPlace,
    FeedingHistory, CaretakerAssignment, VeterinarianAssignment,
    TransferHistory
)
from .serializers import (
    HabitatSerializer, DepartmentSerializer, BuildingSerializer,
    EnclosureSerializer, StaffSerializer, AnimalSerializer,
    FeedingRationTypeSerializer, FeedingRationSerializer,
    ZooSerializer, WinteringPlaceSerializer, FeedingHistorySerializer,
    CaretakerAssignmentSerializer, VeterinarianAssignmentSerializer,
    TransferHistorySerializer
)

# ----------------------------------------------------------------------
# Базовые ViewSet'ы для всех моделей
# ----------------------------------------------------------------------

class HabitatViewSet(viewsets.ModelViewSet):
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Запрос 1: Количество животных в отделе
    @action(detail=False, methods=['get'], url_path='animal-count')
    def animal_count(self, request):
        departments = Department.objects.annotate(animal_count=Count('animals'))
        data = [{'id': d.id, 'name': d.name, 'animal_count': d.animal_count} for d in departments]
        return Response(data)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnclosureViewSet(viewsets.ModelViewSet):
    queryset = Enclosure.objects.all()
    serializer_class = EnclosureSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Запрос 4: Список пустых вольеров
    @action(detail=False, methods=['get'], url_path='empty')
    def empty_enclosures(self, request):
        enclosures = Enclosure.objects.annotate(animal_count=Count('animals')).filter(animal_count=0)
        serializer = self.get_serializer(enclosures, many=True)
        return Response(serializer.data)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeedingRationTypeViewSet(viewsets.ModelViewSet):
    queryset = FeedingRationType.objects.all()
    serializer_class = FeedingRationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeedingRationViewSet(viewsets.ModelViewSet):
    queryset = FeedingRation.objects.all()
    serializer_class = FeedingRationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ZooViewSet(viewsets.ModelViewSet):
    queryset = Zoo.objects.all()
    serializer_class = ZooSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Запрос 5: Отчёт по аренде
    @action(detail=False, methods=['get'], url_path='lease-report')
    def lease_report(self, request):
        # Зоопарки, которые сдают животных в аренду (есть leased_animals с ownership_type='lease')
        report = Zoo.objects.filter(leased_animals__ownership_type='lease').annotate(
            animal_count=Count('leased_animals'),
            total_cost=Sum('leased_animals__lease_cost')
        ).values('id', 'name', 'animal_count', 'total_cost')
        return Response(report)


class WinteringPlaceViewSet(viewsets.ModelViewSet):
    queryset = WinteringPlace.objects.all()
    serializer_class = WinteringPlaceSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Запрос 2: Животные в коммунальных вольерах
    @action(detail=False, methods=['get'], url_path='communal')
    def communal_animals(self, request):
        animals = Animal.objects.filter(current_enclosure__is_communal=True)
        serializer = self.get_serializer(animals, many=True)
        return Response(serializer.data)

    # Запрос 3: Животные в том же здании, что и заданное животное
    @action(detail=True, methods=['get'], url_path='same-building-animals')
    def same_building_animals(self, request, pk=None):
        animal = self.get_object()
        building = animal.current_enclosure.building
        if not building:
            return Response({'error': 'Животное не находится в здании'}, status=400)
        same_building_animals = Animal.objects.filter(
            current_enclosure__building=building
        ).exclude(pk=animal.pk)
        serializer = self.get_serializer(same_building_animals, many=True)
        return Response(serializer.data)


class FeedingHistoryViewSet(viewsets.ModelViewSet):
    queryset = FeedingHistory.objects.all()
    serializer_class = FeedingHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CaretakerAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CaretakerAssignment.objects.all()
    serializer_class = CaretakerAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class VeterinarianAssignmentViewSet(viewsets.ModelViewSet):
    queryset = VeterinarianAssignment.objects.all()
    serializer_class = VeterinarianAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferHistoryViewSet(viewsets.ModelViewSet):
    queryset = TransferHistory.objects.all()
    serializer_class = TransferHistorySerializer
    permission_classes = [permissions.IsAuthenticated]