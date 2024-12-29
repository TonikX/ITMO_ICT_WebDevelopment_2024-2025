import logging

from django.db import models, IntegrityError
from django.db.models import Count, Sum
from django.utils.timezone import now
from djoser.serializers import UserSerializer, User
from rest_framework import viewsets, views, status, generics, permissions, serializers, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (AgentSerializer, EmploymentContractSerializer,
                          OrganizationSerializer, EmployeeSerializer, ContractSerializer, InsuranceCaseSerializer,
                          CustomUserSerializer, InsuranceAgencySerializer, RegisterSerializer, AgentRegisterSerializer,
                          DirectorRegisterSerializer, EmployeeRegisterSerializer, ChangePasswordSerializer,
                          PositionSerializer)

from .models import (Agent, EmploymentContract, Organization, Employee,
                     Contract, InsuranceCase, CustomUser, InsuranceAgency, Position)

logger = logging.getLogger(__name__)

@permission_classes([AllowAny])
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def contract_stats(self, request, pk=None):
        agent = self.get_object()  # get agent by id
        contracts = EmploymentContract.objects.filter(agent=agent)
        total_contracts = contracts.count()
        total_salary = contracts.aggregate(total_salary=models.Sum('salary'))['total_salary']
        return Response({
            'agent_id': agent.id,
            'total_contracts': total_contracts,
            'total_salary': total_salary
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def contracts_count_by_date(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({"error": "start_date and end_date are required"}, status=400)

        contracts_count = Contract.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        ).values('agent', 'contract_type').annotate(count=Count('id'))
        return Response(contracts_count)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_agent(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response(AgentSerializer(agent).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def update_agent(self, request, pk=None):
        agent = self.get_object()
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response(AgentSerializer(agent).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def delete_agent(self, request, pk=None):
        agent = self.get_object()
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        agent = self.get_object()
        contracts = Contract.objects.filter(agent=agent.id)
        agent_data = AgentSerializer(agent).data
        agent_data['contracts'] = ContractSerializer(contracts, many=True).data
        return Response(agent_data)

    # Переопределяем метод list для добавления контрактов ко всем агентам
    def list(self, request, *args, **kwargs):
        agents = Agent.objects.all()
        agent_data = []
        for agent in agents:
            contracts = Contract.objects.filter(agent=agent.id)
            serialized_agent = AgentSerializer(agent).data
            serialized_agent['contracts'] = ContractSerializer(contracts, many=True).data
            agent_data.append(serialized_agent)
        return Response(agent_data)


@permission_classes([AllowAny])
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def agents(self, request, pk=None):
        organization = self.get_object()
        agents = organization.agent_set.all()
        serializer = OrganizationSerializer(agents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def employees(self, request, pk=None):
        organization = self.get_object()
        employees = organization.employee_set.all()
        serializer = OrganizationSerializer(employees, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated])
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def insurance_case_summary(self, request):
        insurance_cases = InsuranceCase.objects.all()
        total_payout_by_contract_type = insurance_cases.values('contract_type').annotate(
            total_payout=models.Sum('payout_amount')
        )
        return Response(total_payout_by_contract_type)

    @action(detail=False, methods=['get'])
    def active_contracts_report(self, request):
        report = Contract.objects.filter(end_date__isnull=False).values(
            'agent__id',
            'agent__first_name',
            'agent__last_name',
            'contract_type'
        ).annotate(
            count=Count('id'),
            total_sum=Sum('total_sum')
        )
        return Response(report)

    @action(detail=False, methods=['get'])
    def view_active_contracts(self, request):
        active_contracts_response = self.active_contracts_report(request)
        return Response({
            'message': 'Active contracts report',
            'data': active_contracts_response.data
        })

    @action(detail=False, methods=['post'])
    def create_contract(self, request):
        data = request.data
        agent_id = data.get('agent')
        organization_id = data.get('organization')
        start_date = data.get('start_date')

        # Check for existing contract
        if Contract.objects.filter(agent_id=agent_id, organization_id=organization_id, start_date=start_date).exists():
            return Response({'error': 'Контракт уже существует с такими данными'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обновление контракта
    @action(detail=True, methods=['patch'])
    def update_contract(self, request, pk=None):
        contract = self.get_object()
        serializer = self.get_serializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Завершение контракта
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def terminate(self, request, pk=None):
        contract = self.get_object()
        contract.delete()
        return Response({'message': 'Контракт удален'}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class InsuranceCaseViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InsuranceCase.objects.all()

    # Проверка, является ли текущий пользователь агентом, который связан с контрактом
    def is_agent_for_case(self, insurance_case):
        # Проверяем существование агента и контракт
        if hasattr(insurance_case.contract, 'agent') and insurance_case.contract.agent:
            return insurance_case.contract.agent.id == self.request.user.id
        return False

    # Создание страхового случая сотрудником
    def create(self, request, *args, **kwargs):
        user = request.user
        # Проверяем, чтобы только сотрудники могли создавать кейсы
        if user.role != 'employee':
            raise PermissionDenied('Only employees can create insurance cases.')

        # Устанавливаем обязательные поля в NULL при создании кейса сотрудником
        data = request.data.copy()
        data['status'] = 'pending'
        data['payout_amount'] = None
        data['payout_decision'] = None

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обновление заявки агентом
    def is_agent_for_case(self, insurance_case):
        agent_id = insurance_case.contract.agent_id
        current_user_id = self.request.user.id
        print(f"Agent ID: {agent_id}, Current User ID: {current_user_id}")

        return insurance_case.contract.agent.user.id == self.request.user.id

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f'Insurance case {instance.id} updated by user {request.user.id}')
        return Response(serializer.data)

    # Суммарные выплаты по типу контракта
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def payout_summary(self, request):
        total_payout_by_type = InsuranceCase.objects.values('contract__contract_type').annotate(
            total_payout=models.Sum('payout_amount')
        )
        return Response(total_payout_by_type)

    # Статистика по статусам кейсов
    @action(detail=False, methods=['get'])
    def case_summary(self, request):
        summary = InsuranceCase.objects.values('status').annotate(total=Count('id'))
        return Response(summary)


@permission_classes([IsAuthenticated])
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'passport_data']

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def insured_employees(self, request, pk=None):
        employee = self.get_object()
        active_contracts = employee.contracts.filter(end_date__gte=models.F('start_date'))
        serializer = EmployeeSerializer(active_contracts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def fire_employee(self, request, pk=None):
        employee = self.get_object()
        employee.delete()
        return Response({'message': 'Employee fired successfully'}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        employee = self.get_object()
        data = request.data.copy()

        # Ensure risk_category is not blank
        if 'risk_category' not in data or not data['risk_category']:
            data['risk_category'] = employee.risk_category

        serializer = self.get_serializer(employee, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):

        user = self.request.user
        queryset = Employee.objects.all()

        # Фильтрация по организации из параметров запроса
        organization = self.request.query_params.get('organization', None)
        if organization:
            queryset = queryset.filter(organization=organization)

        # Если пользователь не админ, ограничиваем по его организации
        if not user.is_superuser:
            if user.role == 'employee' and hasattr(user, 'employee'):
                if not user.employee.position.is_staff:
                    queryset = queryset.filter(organization=user.employee.organization.id)
            else:
                queryset = queryset.none()  # Если пользователь не сотрудник, возвращаем пустой queryset

        return queryset


@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def user_profile(self, request):
        user = request.user
        if user.role == 'agent':
            serializer = AgentSerializer(user)
        elif user.role == 'employee':
            serializer = EmployeeSerializer(user)
        elif user.role == 'org_admin':
            if user.organization:
                serializer = OrganizationSerializer(user.organization)
            else:
                return Response({'error': 'Организация не найдена'}, status=404)
        else:
            serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class RelatedOrganizationsView(views.APIView):
    def get(self, request, organization_id):
        agents = Agent.objects.filter(contract__organization_id=organization_id,
                                      contract__end_date__isnull=True).distinct()
        related_organizations = Organization.objects.filter(
            contract__agent__in=agents,
            contract__end_date__isnull=True
        ).exclude(id=organization_id).distinct()
        serializer = OrganizationSerializer(related_organizations, many=True)
        return Response(serializer.data)


class ContractsCountByTypeView(views.APIView):
    def get(self, request, start_date, end_date):
        contracts_count = Contract.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        ).values('agent', 'contract_type').annotate(count=Count('id'))
        return Response(contracts_count)


@permission_classes([AllowAny])
class InsuredEmployeesView(views.APIView):
    def get(self, request, person_id):
        contracts = Contract.objects.filter(
            agent__id=person_id
        )
        insured_employees = Employee.objects.filter(contract__in=contracts).distinct()
        serializer = EmployeeSerializer(insured_employees, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class TotalPayoutsByContractTypeView(views.APIView):
    def get(self, request, start_date, end_date):
        payouts = InsuranceCase.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('contract__contract_type').annotate(total_payout=Sum('payout_amount'))
        return Response(payouts)


class ContractDetailsAndTotalPayoutsView(views.APIView):
    def get(self, request):
        contract_details = Contract.objects.values(
            'organization__full_name',
            'id',
            'start_date',
            'end_date',
            'total_sum'
        ).annotate(total_payout=Sum('insurancecase__payout_amount'))
        return Response(contract_details)


class EmployeeContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        agency = validated_data.pop('agency', None)  # Убираем agency из validated_data
        payout_amount = validated_data.pop('payout_amount', 0)
        position = validated_data.pop('position', None)

        # Создаем пользователя
        user = CustomUser.objects.create_user(**validated_data)

        # Если это агент, создаем запись в модели Agent
        if user.role == 'agent':
            agent, _ = Agent.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': user.username,
                    'passport_data': validated_data.get('passport_data', ''),
                    'contact_info': validated_data.get('contact_info', '')
                }
            )
            # Привязка агента к агентству через ManyToManyField
            if agency:
                agency.agents.add(agent)

        # Если сотрудник - создаем Employee
        elif user.role == 'employee':
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': user.username,
                    'age': validated_data.get('age', 18),
                    'position_id': position.id if position else None,
                    'organization': user.organization,
                    'passport_data': validated_data.get('passport_data', ''),
                    'payout_amount': payout_amount
                }
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)


class AgentRegisterView(RegisterView):
    serializer_class = AgentRegisterSerializer
    role = 'agent'  # Роль для агентов


class EmployeeRegisterView(RegisterView):
    serializer_class = EmployeeRegisterSerializer
    role = 'employee'  # Роль для сотрудников


class DirectorRegisterView(RegisterView):
    serializer_class = DirectorRegisterSerializer
    role = 'org_admin'


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Личный кабинет Агента
class AgentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'agent':
            return Response({"error": "Access denied"}, status=403)

        contracts = Contract.objects.filter(agent=request.user.agent)
        contracts_data = ContractSerializer(contracts, many=True).data

        return Response({
            "message": "Welcome to the Agent Dashboard",
            "username": request.user.username,
            "email": request.user.email,
            "contracts": contracts_data
        })


# Личный кабинет Сотрудника
class EmployeeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Проверяем, что у пользователя есть профиль сотрудника
            employee = Employee.objects.get(user=request.user)

            # Фильтруем контракты, где сотрудник участвует
            active_contracts = Contract.objects.filter(
                employees=employee,
                end_date__gte=now().date()  # Только активные контракты
            )

            # Если контрактов нет
            if not active_contracts.exists():
                return Response({
                    "username": request.user.username,
                    "message": "У вас нет активных контрактов."
                })

            # Если контракты есть, сериализуем их
            contracts_data = ContractSerializer(active_contracts, many=True).data
            return Response({
                "username": request.user.username,
                "contracts": contracts_data
            })

        except Employee.DoesNotExist:
            return Response({
                "error": "Профиль сотрудника не найден."
            }, status=404)


# Личный кабинет Директора (Администратора Организации)
class DirectorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'org_admin':
            return Response({"error": "Access denied"}, status=403)

        organization = request.user.organization
        employees = Employee.objects.filter(organization=organization)
        contracts = Contract.objects.filter(organization=organization)

        employees_data = EmployeeSerializer(employees, many=True).data
        contracts_data = ContractSerializer(contracts, many=True).data

        return Response({
            "message": "Welcome to the Director Dashboard",
            "username": request.user.username,
            "email": request.user.email,
            "organization": organization.full_name,
            "employees": employees_data,
            "contracts": contracts_data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def fire_employee(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.organization = None  # Убираем сотрудника из организации
            employee.save()
            return Response({"message": f"{employee.first_name} {employee.last_name} was fired."}, status=200)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)


# Обновление пароля
class ChangePasswordView(generics.UpdateAPIView):
    model = CustomUser
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password"}, status=400)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password updated successfully"}, status=200)
        return Response(serializer.errors, status=400)


@permission_classes([AllowAny])
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@permission_classes([AllowAny])
class AgencyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceAgency.objects.all()
    serializer_class = InsuranceAgencySerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_superuser:
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "admin",
                "message": "Superuser has access to all data."
            })

        # Логика для сотрудников
        if user.role == 'employee':
            try:
                employee = user.employee
                return Response({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "organization": employee.organization.full_name if employee.organization else None,
                    "organization_id": user.employee.organization.id,
                    "position": {
                        'name': employee.position.name if employee.position else None,
                        'is_staff': employee.position.is_staff if employee.position else False
                    }
                })
            except Employee.DoesNotExist:
                return Response({"error": "Employee profile not found."}, status=404)

        # Логика для агентов
        if user.role == 'agent':
            try:
                agent = user.agent
                return Response({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "agency": agent.agencies.first().name if agent.agencies.exists() else None
                })
            except Agent.DoesNotExist:
                return Response({"error": "Agent profile not found."}, status=404)

        return Response({"error": "User role not recognized."}, status=400)


class ContractCreateView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        # Проверяем, есть ли профиль сотрудника
        if not hasattr(user, 'employee'):
            raise serializers.ValidationError({'error': 'Вы не являетесь сотрудником.'})

        employee = user.employee

        # Проверяем права: is_staff
        if not employee.position.is_staff:
            raise serializers.ValidationError({'error': 'Недостаточно прав для создания контракта.'})

        # Получаем организацию сотрудника
        organization = employee.organization
        if not organization:
            raise serializers.ValidationError({'error': 'Вы не привязаны к организации.'})

        # Проверка на наличие существующего контракта (агент + организация + дата начала)
        existing_contract = Contract.objects.filter(
            agent=user.agent if hasattr(user, 'agent') else None,
            organization=organization,
            start_date=now().date()
        ).first()

        if existing_contract:
            # Если контракт уже есть, обновляем данные
            serializer.update(existing_contract, serializer.validated_data)
            existing_contract.employees.add(employee)  # Добавляем директора в контракт
            return Response(
                {'message': 'Контракт обновлен.', 'contract_id': existing_contract.id},
                status=status.HTTP_200_OK
            )

        # Фильтрация сотрудников для включения в контракт
        employees = Employee.objects.filter(organization=organization)
        if not employees.exists():
            raise serializers.ValidationError({'error': 'В организации нет сотрудников.'})

        # Создание нового контракта
        try:
            contract = serializer.save(
                agent=user.agent if hasattr(user, 'agent') else None,
                organization=organization,
                start_date=now().date()
            )
            contract.employees.set(employees)  # Добавляем всех сотрудников
            contract.employees.add(employee)  # Добавляем директора отдельно
            return Response(
                {'message': 'Контракт успешно создан.', 'contract_id': contract.id},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Ошибка сохранения контракта.'})


class UserPartialUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Исключаем организацию и должность из обновляемых полей
        excluded_fields = ['organization', 'position']
        for field in excluded_fields:
            if field in request.data:
                del request.data[field]

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
