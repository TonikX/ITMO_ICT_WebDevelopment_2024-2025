from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Count, Avg
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from .permissions import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated
from .models import Diet, Breed, Hen, Cage, Workshop, Employee
from .serializers import (
    DietSerializer,
    BreedSerializer,
    HenSerializer,
    CageSerializer,
    WorkshopSerializer,
    EmployeeSerializer
)


class DietListView(ListAPIView):
    """
    Список всех Diet
    """
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    

class DietDetailView(RetrieveAPIView):
    """
    Детальная информация о Diet
    """
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class DietCreateView(CreateAPIView):
    """
    Создание новой Diet
    """
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [IsAdminOrManager]


class DietUpdateView(UpdateAPIView):
    """
    Обновление существующей Diet
    """
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [IsAdminOrManager]


class DietDeleteView(DestroyAPIView):
    """
    Удаление Diet
    """
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [IsAdminOrManager]


class BreedListView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class BreedDetailView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class BreedCreateView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAdminOrManager]


class BreedUpdateView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAdminOrManager]


class BreedDeleteView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAdminOrManager]


class HenListView(ListAPIView):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class HenDetailView(RetrieveAPIView):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class HenCreateView(CreateAPIView):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [IsAdminOrManager]


class HenUpdateView(UpdateAPIView):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [IsAdminOrManager]


class HenDeleteView(DestroyAPIView):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [IsAdminOrManager]


class CageListView(ListAPIView):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class CageDetailView(RetrieveAPIView):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class CageCreateView(CreateAPIView):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [IsAdminOrManager]


class CageUpdateView(UpdateAPIView):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [IsAdminOrManager]


class CageDeleteView(DestroyAPIView):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [IsAdminOrManager]


class WorkshopListView(ListAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class WorkshopDetailView(RetrieveAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class WorkshopCreateView(CreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAdminOrManager]


class WorkshopUpdateView(UpdateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAdminOrManager]


class WorkshopDeleteView(DestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeDetailView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeCreateView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeUpdateView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeDeleteView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]


class HenEggsCountView(APIView):
    """
    Получить количество яиц от каждой курицы данного веса, породы, возраста
    """
    permission_classes = [IsAdminOrManager]
    def get(self, request, *args, **kwargs):
        
        weight = request.query_params.get('weight')
        breed = request.query_params.get('breed')
        age = request.query_params.get('age')

        hens = Hen.objects.all()

        if weight is not None:
            hens = hens.filter(weight=weight)

        if breed is not None:
            hens = hens.filter(breed__name=breed)

        if age is not None:
            hens = hens.filter(age=age)

        # Собираем результат
        hens_data = hens.values('id', 'weight', 'breed__name', 'age', 'eggs_per_month')

        return Response(hens_data, status=status.HTTP_200_OK)


class MaxHenByWorkshopView(APIView):
    """
    Получить цех с наибольшим количеством кур для каждой породы
    """
    permission_classes = [IsAdminOrManager]
    def get(self, request, *args, **kwargs):
        breeds = Breed.objects.all()
        result = []

        for breed in breeds:
            workshops = Hen.objects.filter(breed=breed).values('cage__workshop__id').annotate(
                total_hens=Count('id')
            ).order_by('-total_hens')

            if workshops:
                result.append({
                    'breed': breed.name,
                    'workshop': workshops[0]['cage__workshop__id'],
                    'total_hens': workshops[0]['total_hens']
                })

        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response({"detail": "No data found"}, status=status.HTTP_404_NOT_FOUND)


class AvgEggsPerEmployeeView(APIView):
    """
    Среднее количество яиц, которое получает в день каждый работник от обслуживаемых им кур
    """
    permission_classes = [IsAdminOrManager]
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all().values('id').annotate(
            avg_eggs=Avg(F('assigned_cages__hens__eggs_per_month') / 30)
        )
        
        return Response(employees, status=status.HTTP_200_OK)
    

class HensCountByBreedAndWorkshopView(APIView):
    """
    Сколько кур каждой породы в каждом цехе
    """
    permission_classes = [IsAdminOrManager]
    def get(self, request, *args, **kwargs):
        data = Hen.objects.values('cage__workshop__id', 'breed__name').annotate(
            total_hens=Count('id')
        )

        return Response(data, status=status.HTTP_200_OK)
    

class BreedVsFactoryAverageView(APIView):
    """
    Разница между показателями породы и средними показателями по птицефабрике
    """
    permission_classes = [IsAdminOrManager]
    def get(self, request, *args, **kwargs):
        factory_avg_eggs = Hen.objects.aggregate(
            avg_eggs=Avg('eggs_per_month')
        )['avg_eggs']

        breeds = Breed.objects.all()
        breed_data = []

        for breed in breeds:
            breed_avg_eggs = Hen.objects.filter(breed=breed).aggregate(
                avg_eggs=Avg('eggs_per_month')
            )['avg_eggs']
            if breed_avg_eggs is not None:
                breed_data.append({
                    'breed': breed.name,
                    'avg_eggs_breed': breed_avg_eggs,
                    'diff_from_factory': breed_avg_eggs - factory_avg_eggs
                })

        return Response(breed_data, status=status.HTTP_200_OK)

