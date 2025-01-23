# API Endpoints Documentation

## Регистрация пользователя
**POST** `/register_user/`
- **Summary:** Регистрация пользователя
- **Description:** Этот эндпоинт позволяет создать нового пользователя в системе, отправив необходимые данные в формате `UserRegistrationSerializer`.
- **Request Body:** `UserRegistrationSerializer`
- **Responses:**
  - `201`: Пользователь успешно зарегистрирован
  - `400`: Ошибки валидации
  - 
```python
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
```

## Вход пользователя
**POST** `/login_user/`
- **Summary:** Вход пользователя
- **Description:** Этот эндпоинт позволяет пользователю войти в систему, используя свои учетные данные.
- **Request Body:** `UserLoginSerializer`
- **Responses:**
  - `200`: Успешный вход
  - `400`: Ошибки валидации
  - `401`: Неверные учетные данные
  - 
```python
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
```

## Выход пользователя
**POST** `/logout_user/`
- **Summary:** Выход пользователя
- **Description:** Этот эндпоинт позволяет пользователю выйти из системы.
- **Responses:**
  - `200`: Выход успешен

```python
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
```

## Получить список концертов
**GET** `/concert_list/`
- **Summary:** Получить список концертов
- **Description:** Этот эндпоинт возвращает список всех доступных концертов.
- **Responses:**
  - `200`: `ConcertSerializer(many=True)`

```python
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
```

## Получить информацию о концерте
**GET** `/concert_detail/<pk>/`
- **Summary:** Получить информацию о концерте
- **Description:** Этот эндпоинт предоставляет подробную информацию о конкретном концерте по его идентификатору.
- **Responses:**
  - `200`: `ConcertDetailSerializer`
  - `404`: Концерт не найден

```python
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
```

## Создание билета
**POST** `/ticket_list_create/`
- **Summary:** Создание билета
- **Description:** Этот эндпоинт позволяет пользователям создавать новый билет для концерта.
- **Request Body:** `TicketCreateSerializer`
- **Responses:**
  - `201`: `TicketSerializer`
  - `400`: Ошибки валидации
  - `403`: Недостаточно прав

```python
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
```

## Обновление, частичное обновление и удаление билета
**GET, PUT, PATCH, DELETE** `/ticket_detail/<pk>/`
- **Summary:** Получение, обновление, или удаление билета
- **Description:** Этот эндпоинт позволяет пользователям просматривать, обновлять или удалять билет по его идентификатору.
- **Request Body (for PUT, PATCH):** `TicketSerializer`
- **Responses:**
  - `200`: `TicketSerializer`
  - `204`: Билет удален
  - `400`: Ошибки валидации
  - `403`: Недостаточно прав
  - `404`: Билет не найден

```python
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
    responses={200: TicketSerializer, 404: "Билет не найден"}
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
```

## Создание заказа
**POST** `/order_list_create/`
- **Summary:** Создание заказа
- **Description:** Этот эндпоинт позволяет пользователю создавать новый заказ на билеты для концерта.
- **Request Body:** `OrderCreationSerializer`
- **Responses:**
  - `201`: `OrderCreationSerializer`
  - `400`: Ошибки валидации

```python
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
```

## Подтверждение заказа
**POST** `/confirm_order/<pk>/`
- **Summary:** Подтверждение заказа
- **Description:** Этот эндпоинт позволяет администраторам подтверждать заказы пользователей.
- **Responses:**
  - `200`: Заказ подтвержден
  - `404`: Заказ не найден

```python
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
```

## Создать концерт
**POST** `/create_concert/`
- **Summary:** Создать концерт
- **Description:** Этот эндпоинт позволяет администраторам добавлять новый концерт в систему.
- **Request Body:** `ConcertSerializer`
- **Responses:**
  - `201`: `ConcertSerializer`
  - `400`: Ошибки валидации

```python
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
```

## Удалить концерт
**DELETE** `/delete_concert/<pk>/`
- **Summary:** Удалить концерт
- **Description:** Этот эндпоинт позволяет администраторам удалять концерт по его идентификатору.
- **Responses:**
  - `204`: Концерт удален
  - `404`: Концерт не найден

```python
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
```

## Редактировать концерт
**PUT** `/update_concert/<pk>/`
- **Summary:** Редактировать концерт
- **Description:** Этот эндпоинт позволяет администраторам обновлять информацию о существующем концерте.
- **Request Body:** `ConcertSerializer`
- **Responses:**
  - `200`: `ConcertSerializer`
  - `400`: Ошибки валидации
  - `404`: Концерт не найден

```python
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
```

## Получить конкретный заказ
**GET** `/get_order/<pk>/`
- **Summary:** Получить конкретный заказ
- **Description:** Этот эндпоинт предоставляет информацию о конкретном заказе по его идентификатору.
- **Responses:**
  - `200`: `OrderSerializer`
  - `404`: Заказ не найден

```python
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
```

## Добавить оборудование для концерта
**POST** `/add_equipment_to_concert/`
- **Summary:** Добавить оборудование для концерта
- **Description:** Этот эндпоинт позволяет администраторам добавлять оборудование к конкретному концерту.
- **Request Body:** `ConcertEquipmentSerializer`
- **Responses:**
  - `201`: `ConcertEquipmentSerializer`
  - `400`: Ошибки валидации

```python
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
```

## Удалить оборудование из концерта
**DELETE** `/remove_equipment_from_concert/<pk>/`
- **Summary:** Удалить оборудование из концерта
- **Description:** Этот эндпоинт позволяет администраторам удалять оборудование из концерта по его идентификатору.
- **Responses:**
  - `204`: Оборудование удалено
  - `404`: Оборудование не найдено

```python
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
```

## Редактировать оборудование для концерта
**PUT** `/update_equipment_for_concert/<pk>/`
- **Summary:** Редактировать оборудование для концерта
- **Description:** Этот эндпоинт позволяет администраторам обновлять информацию об оборудовании для концерта.
- **Request Body:** `ConcertEquipmentSerializer`
- **Responses:**
  - `200`: `ConcertEquipmentSerializer`
  - `400`: Ошибки валидации
  - `404`: Оборудование не найдено

```python
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
```

## Получить оборудование для концерта
**GET** `/get_equipment_for_concert/<concert_id>/`
- **Summary:** Получить оборудование для концерта
- **Description:** Этот эндпоинт предоставляет список оборудования, назначенного для конкретного концерта.
- **Responses:**
  - `200`: `ConcertEquipmentSerializer(many=True)`
  - `404`: Концерт не найден

```python
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
```

## Назначить концерт организатору
**POST** `/assign_concert/<pk>/`
- **Summary:** Назначить концерт организатору
- **Description:** Этот эндпоинт позволяет назначить концерт определенному организатору.
- **Request Body:** `OrganizerSerializer`
- **Responses:**
  - `200`: Концерт успешно назначен организатору
  - `400`: Ошибка в запросе
  - `404`: Концерт не найден
  - `403`: Недостаточно прав

```python
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
```

## Получение всех концертов организатора
**GET** `/get_organizer_concerts/`
- **Summary:** Получение всех концертов организатора
- **Description:** Этот эндпоинт возвращает список всех концертов, назначенных текущему организатору.
- **Responses:**
  - `200`: `ConcertDetailSerializer(many=True)`
  - `403`: Недостаточно прав
  - `400`: Ошибка запроса

```python
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
    if not hasattr(request.user, "employee"):
        return Response({"error": "Пользователь не является сотрудником"}, status=status.HTTP_403
