from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F
from rest_framework.generics import *
from .models import *
from .serializers import *


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


# Пользователи
class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Газеты
class NewspaperCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


class NewspaperListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


class NewspaperDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperDetailSerializer


class NewspaperUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


class NewspaperDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Newspaper.objects.all()
    serializer_class = NewspaperSerializer


# Типографии
class PrintingHouseCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer


class PrintingHouseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer


class PrintingHouseDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseDetailSerializer


class PrintingHouseUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer


class PrintingHouseDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = PrintingHouse.objects.all()
    serializer_class = PrintingHouseSerializer


# Почтовые отделения
class PostOfficeCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer


class PostOfficeListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer


class PostOfficeDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeDetailSerializer


class PostOfficeUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer


class PostOfficeDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer


# Тиражи
class EditionCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class EditionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class EditionDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class EditionUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class EditionDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


# Поставки
class DistributionCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class DistributionDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


# Запросы с аналитикой
class NewspaperAddressesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        newspaper_name = request.data.get('name')
        if not newspaper_name:
            return Response({"error": "Название газеты не указано"}, status=400)

        addresses = Edition.objects.filter(newspaper__name=newspaper_name).values_list('printing_house__address',
                                                                                       flat=True).distinct()
        return Response({"addresses": list(addresses)})


class TopEditorByPrintingHouseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        printing_house_id = request.data.get('printing_house_id')
        if not printing_house_id:
            return Response({"error": "ID типографии не указан"}, status=400)

        result = (Edition.objects.filter(printing_house_id=printing_house_id)
                  .values(
            editor_id=F('newspaper__editor__id'),
            editor_name=F('newspaper__editor__last_name'),
            editor_first_name=F('newspaper__editor__first_name')
        )
                  .annotate(total_quantity=Sum('quantity'))
                  .order_by('-total_quantity')
                  .first())

        return Response({
            "editor_id": result.get('editor_id') if result else None,
            "editor_name": f"{result.get('editor_first_name', '')} {result.get('editor_name', '')}".strip() if result else None,
            "total_quantity": result.get('total_quantity', 0) if result else 0
        })


class ExpensiveNewspaperOfficesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        min_price = request.data.get('min_price')
        if not min_price:
            return Response({"error": "Минимальная цена не указана"}, status=400)

        offices = Distribution.objects.filter(newspaper__price__gt=min_price).values(
            post_office_address=F('post_office__address'),
            newspaper_name=F('newspaper__name')
        ).distinct()
        return Response({"offices": list(offices)})


class LowQuantityDistributionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        max_quantity = request.data.get('max_quantity')
        if not max_quantity:
            return Response({"error": "Максимальное количество не указано"}, status=400)

        distributions = Distribution.objects.filter(quantity__lt=max_quantity).values(
            'newspaper__name', 'post_office__number', 'quantity'
        )
        return Response({"distributions": list(distributions)})


class NewspaperDestinationByAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        newspaper_name = request.data.get('name')
        printing_house_address = request.data.get('address')
        if not newspaper_name or not printing_house_address:
            return Response({"error": "Название газеты или адрес типографии не указаны"}, status=400)

        destinations = Distribution.objects.filter(
            newspaper__name=newspaper_name,
            printing_house__address=printing_house_address
        ).values('post_office__address', 'quantity')
        return Response({"destinations": list(destinations)})


# Отчеты
class PrintingHouseReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        printing_house_id = request.data.get('printing_house_id')
        if not printing_house_id:
            return Response({"error": "ID типографии не указан"}, status=400)

        printing_house = PrintingHouse.objects.filter(id=printing_house_id).first()
        if not printing_house:
            return Response({"error": "Типография не найдена"}, status=404)

        # Общее количество газет в типографии
        total_newspapers = Edition.objects.filter(printing_house=printing_house).aggregate(total=Sum('quantity'))[
                               'total'] or 0

        # Количество газет каждого наименования
        newspaper_counts = Edition.objects.filter(printing_house=printing_house).values(
            newspaper_name=F('newspaper__name')
        ).annotate(quantity=Sum('quantity'))

        # Распределение газет по почтовым отделениям
        distributions = Distribution.objects.filter(printing_house=printing_house).values(
            newspaper_name=F('newspaper__name'),
            post_office_address=F('post_office__address')
        ).annotate(quantity=Sum('quantity'))

        response = {
            "printing_house": {
                "id": printing_house.id,
                "name": printing_house.name,
                "address": printing_house.address
            },
            "total_newspapers": total_newspapers,
            "newspaper_counts": list(newspaper_counts),
            "distributions": list(distributions)
        }

        return Response(response)
