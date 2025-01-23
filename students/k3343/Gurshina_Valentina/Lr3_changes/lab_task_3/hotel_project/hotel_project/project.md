Документация по лабораторной работе №3:

Расссмотрим имеющиееся классы и методы API:

1. ClientsAPIView

```
class ClientsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
```
Используем класс для работы с клиентами. Наследуем его от GenericAPIView. Возможна аутентификация только для авторизованных пользователей. Используем сериализатор ClientSerializer. 

``
def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response({"Clients": serializer.data})

    def post(self, request):
        client = request.data.get('client')
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid(raise_exception=True):
            client_saved = serializer.save()
        return Response({"Success": "Client '{}' implemented succesfully.".format(client_saved.full_name)})
``

Методы get & post:

С помощью метода get получаем всех клиентов из базы данных. С помощью сериалайзера преобразуем их в JSON. И возвращаем результат. 
С помощью метода post получаем данные клиента из запроса. Проверяем через сериалайзер их точность и соответствие. Сохраняет данные в базу и возвращает сообщение об успешном сохранении. 

2. RoomsAPIView

``
class RoomsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

``

Это представление нам необходимо для получения списка всех комнат. Наследуется от ListAPIView и возвращает список объектов Room.

3. RoomsDetailsAPIView

``
class RoomDetailsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'

``

Представление для получения деталей конкретной комнаты по id. Наследуется от RetrieveAPIView.

4. ReservationsAPIView

Необходим для обработки бронирований (Reservations). 

``
class ReservationsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response({"Reservations": serializer.data})

    def post(self, request):
        admin_id = request.user.pk
        reservation = dict()
        room = request.data.get('room')
        client = request.data.get('client')
        arrival_date = request.data.get('arrival_date')
        departure_date = request.data.get('departure_date')
        reservation['admin'] = admin_id
        reservation['client'] = client
        reservation['arrival_date'] = arrival_date
        reservation['departure_date'] = departure_date
        reservation['room'] = room
        serializer = SuperUserSerializer(data=reservation)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"Congratulations!": "Reservation implemented successfully."})

``

Методы GET & POST: (1) получает все бронирования и возвращает их. (2) Создает бронирование на основе данных из запроса. Сохраняет инфо через SuperUserSerializer. 

5. EmployeesAPIView

Оработка запросов, связанных с сотрудниками(Employee).

``
class EmployeesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"Employees": serializer.data})

    def post(self, request):
        employee = request.data.get('employee')
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee_saved = serializer.save()
        return Response({"Congratulations!": "Employee '{}' added successfully.".format(employee_saved.full_name)})

``

Методы GET & POST: (1) Возвращает список всех сотрудников. (2) Создание нового сотрудника и сохранение его. 

Аналогично вышеописанным представлениям, выполняется и прописывается логика для многих оставшихся. 

6. FreeRoomsAPIView

``
class FreeRoomsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"The number of free rooms: ": Reservation.objects.filter(departure_date__lte=datetime.now()).count()})

``

Происходит расчет по текущей дате количества свободных комнат. 

7. ReportAPIView(APIView)

```

class ReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Receive the report for specific quarter.", #отчет по конкретному кварталу/промежутку времени
        manual_parameters=[
            openapi.Parameter(
                'quarter',
                openapi.IN_QUERY,
                description="The number of quarter",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful search", schema=EmployeeSerializer),
        }
    )

    def get(self, request):
        print(request.data)
        quarter = int(request.query_params.get('quarter'))
        print(quarter)
        if not (1 <= quarter <= 4):
            raise BadRequest("Введите правильный номер квартала (от 1 до 4)")

        current_year = timezone.now().year 
        #создание логики кварталов
        quarter_start_month = 3 * (quarter - 1) + 1
        quarter_end_month = 3 * quarter

        quarter_start = date(
            year=current_year,
            month=quarter_start_month,
            day=1,
        )

        quarter_end = date(
            year=current_year,
            month=quarter_end_month,
            day=calendar.monthrange(current_year, quarter_end_month)[1],
        )

        report = {
            "clients_per_room": self._get_clients_per_room(quarter_start, quarter_end),
            "rooms_per_floor": self._get_rooms_per_floor(),
            "profit_per_room": self._get_profit_per_room(quarter_start, quarter_end),
            "total_profit": self._calculate_total_profit(quarter_start, quarter_end),
        }

        return Response(report)`
```
Проверяем корректность данных квартала. Вычисляем начало и конец квартала. Формируем отчет с метриками. 