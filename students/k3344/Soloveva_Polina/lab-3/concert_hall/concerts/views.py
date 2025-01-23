from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .models import Concert, Ticket, Order, Organizer, ConcertEquipment
from .serializers import (
    ConcertSerializer, ConcertDetailSerializer, TicketSerializer,
    TicketCreateSerializer, OrderSerializer, OrganizerSerializer,
    UserRegistrationSerializer, UserLoginSerializer, OrderCreationSerializer, ConcertEquipmentSerializer
)


@swagger_auto_schema(
    method="post",
    operation_summary="Регистрация пользователя",
    request_body=UserRegistrationSerializer,
    responses={201: "Пользователь успешно зарегистрирован", 400: "Ошибки валидации"},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(username=serializer.validated_data["username"]).exists():
            return Response({"error": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(**serializer.validated_data)
        return Response({"message": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    operation_summary="Вход пользователя",
    request_body=UserLoginSerializer,
    responses={200: "Успешный вход", 400: "Ошибки валидации", 401: "Неверные учетные данные"},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
    return Response({"error": "Неверное имя пользователя или пароль"}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method="post",
    operation_summary="Выход пользователя",
    responses={200: "Выход успешен"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.auth.delete()
    return Response({"message": "Вы успешно вышли"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    operation_summary="Получить список концертов",
    responses={200: ConcertSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def concert_list(request):
    concerts = Concert.objects.all()
    serializer = ConcertSerializer(concerts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    operation_summary="Получить информацию о концерте",
    responses={200: ConcertDetailSerializer, 404: "Концерт не найден"}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def concert_detail(request, pk):
    try:
        concert = Concert.objects.get(pk=pk)
    except Concert.DoesNotExist:
        return Response({"error": "Концерт не найден"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConcertDetailSerializer(concert)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    operation_summary="Создание билета",
    request_body=TicketCreateSerializer,
    responses={201: TicketSerializer, 400: "Ошибки валидации", 403: "Недостаточно прав"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def ticket_list_create(request):
    serializer = TicketCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="put",
    operation_summary="Обновление билета",
    request_body=TicketSerializer,
    responses={200: TicketSerializer, 400: "Ошибки валидации", 403: "Недостаточно прав", 404: "Билет не найден"}
)
@swagger_auto_schema(
    method="patch",
    operation_summary="Частичное обновление билета",
    request_body=TicketSerializer,
    responses={200: TicketSerializer, 400: "Ошибки валидации", 403: "Недостаточно прав", 404: "Билет не найден"}
)
@swagger_auto_schema(
    method="delete",
    operation_summary="Удаление билета",
    responses={204: "Билет удален", 403: "Недостаточно прав", 404: "Билет не найден"}
)
@swagger_auto_schema(
    method="get",
    operation_summary="Получение информации о билете",
    responses={204: "Билет удален", 403: "Недостаточно прав", 404: "Билет не найден"}
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def ticket_detail(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Билет не найден"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(TicketSerializer(ticket).data)

    if not request.user.is_staff:
        return Response({"error": "Недостаточно прав"}, status=status.HTTP_403_FORBIDDEN)

    if request.method in ["PUT", "PATCH"]:
        serializer = TicketSerializer(ticket, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ticket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method="post",
    operation_summary="Создание заказа",
    request_body=OrderCreationSerializer,
    responses={201: OrderCreationSerializer, 400: "Ошибки валидации"}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    serializer = OrderCreationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method="post",
    operation_summary="Подтверждение заказа",
    responses={200: "Заказ подтвержден", 404: "Заказ не найден"}
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def confirm_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

    order.status = "confirmed"
    order.save()
    return Response({"status": "Order confirmed"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    operation_summary="Создать концерт",
    request_body=ConcertSerializer,
    responses={201: ConcertSerializer, 400: "Ошибки валидации"}
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_concert(request):
    serializer = ConcertSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="delete",
    operation_summary="Удалить концерт",
    responses={204: "Концерт удален", 404: "Концерт не найден"}
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_concert(request, pk):
    try:
        concert = Concert.objects.get(pk=pk)
        concert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Concert.DoesNotExist:
        return Response({"error": "Концерт не найден"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="put",
    operation_summary="Редактировать концерт",
    request_body=ConcertSerializer,
    responses={200: ConcertSerializer, 400: "Ошибки валидации", 404: "Концерт не найден"}
)
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_concert(request, pk):
    try:
        concert = Concert.objects.get(pk=pk)
    except Concert.DoesNotExist:
        return Response({"error": "Концерт не найден"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConcertSerializer(concert, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_summary="Получить конкретный заказ",
    responses={200: OrderSerializer, 404: "Заказ не найден"}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        return Response(OrderSerializer(order).data)
    except Order.DoesNotExist:
        return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="post",
    operation_summary="Добавить оборудование для концерта",
    request_body=ConcertEquipmentSerializer,
    responses={201: ConcertEquipmentSerializer, 400: "Ошибки валидации"}
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_equipment_to_concert(request):
    serializer = ConcertEquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="delete",
    operation_summary="Удалить оборудование из концерта",
    responses={204: "Оборудование удалено", 404: "Оборудование не найдено"}
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def remove_equipment_from_concert(request, pk):
    try:
        equipment = ConcertEquipment.objects.get(pk=pk)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ConcertEquipment.DoesNotExist:
        return Response({"error": "Оборудование не найдено"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="put",
    operation_summary="Редактировать оборудование для концерта",
    request_body=ConcertEquipmentSerializer,
    responses={200: ConcertEquipmentSerializer, 400: "Ошибки валидации", 404: "Оборудование не найдено"}
)
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_equipment_for_concert(request, pk):
    try:
        equipment = ConcertEquipment.objects.get(pk=pk)
    except ConcertEquipment.DoesNotExist:
        return Response({"error": "Оборудование не найдено"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConcertEquipmentSerializer(equipment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_summary="Получить оборудование для концерта",
    responses={200: ConcertEquipmentSerializer(many=True), 404: "Концерт не найден"}
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_equipment_for_concert(request, concert_id):
    try:
        concert = Concert.objects.get(pk=concert_id)
    except Concert.DoesNotExist:
        return Response({"error": "Концерт не найден"}, status=status.HTTP_404_NOT_FOUND)

    concert_equipment = ConcertEquipment.objects.filter(concert=concert)

    return Response(ConcertEquipmentSerializer(concert_equipment, many=True).data)


@swagger_auto_schema(
    method="post",
    operation_summary="Назначить концерт организатору",
    request_body=OrganizerSerializer,
    responses={
        200: "Концерт успешно назначен организатору",
        400: "Ошибка в запросе",
        404: "Концерт не найден",
        403: "Недостаточно прав"
    }
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def assign_concert(request, pk=None):
    # Проверяем, есть ли у пользователя связанный сотрудник
    if not hasattr(request.user, "employee"):
        return Response({"error": "У пользователя нет связанного сотрудника"}, status=status.HTTP_403_FORBIDDEN)

    try:
        concert = Concert.objects.get(pk=pk)
    except Concert.DoesNotExist:
        return Response({"error": "Концерт не найден"}, status=status.HTTP_404_NOT_FOUND)

    try:
        Organizer.objects.create(employee=request.user.employee, concert=concert)
    except Exception as e:
        return Response({"error": f"Ошибка при назначении концерта: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"status": "Концерт успешно назначен организатору"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    operation_summary="Получение всех концертов организатора",
    responses={
        200: ConcertDetailSerializer(many=True),
        403: "Недостаточно прав",
        400: "Ошибка запроса"
    }
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_organizer_concerts(request):
    # Проверяем, есть ли у пользователя связанный сотрудник
    if not hasattr(request.user, "employee"):
        return Response({"error": "Пользователь не является сотрудником"}, status=status.HTTP_403_FORBIDDEN)

    concerts = Concert.objects.filter(organizers__employee=request.user.employee).distinct()

    return Response(ConcertDetailSerializer(concerts, many=True).data, status=status.HTTP_200_OK)


