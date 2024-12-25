from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework import generics


class ClientListCreateView(generics.ListCreateAPIView):
    """
    Получение полного списка клиентов (GET запрос),
    а также  добавление клиентов (POST запрос)
    """
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientListSerializer
        elif self.request.method == 'POST':
            return ClientSerializer


class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельными клиентами: вывод информации,
    редактирование, удаление
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = "id"


class SpecializationListCreateAPIView(generics.ListCreateAPIView):
    """
    Добавление и список всех возможных специализаций компаний
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class EnterpriseListCreateAPIView(generics.ListCreateAPIView):
    """
    Добавление и список компаний
    """
    queryset = Enterprise.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EnterpriseListSerializer
        elif self.request.method == 'POST':
            return EnterpriseSerializer


class EnterpriseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельной компанией: информация, изменение, удаление
    """
    queryset = Enterprise.objects.all()
    lookup_field = "id"
    serializer_class = EnterpriseSerializer


class EmployeeContractListCreateAPIView(generics.ListCreateAPIView):
    """
    Получение информации о списке контрактов с агентами, а также их добавление
    """
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer


class EmployeeContractUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельным рабочим контрактом: просмотр, редактирование, удаление
    """
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
    lookup_field = "id"


class AgentListAPIView(generics.ListAPIView):
    """
    Получение списка агентов
    Добавление происходит через регистрацию по токенам
    """
    queryset = Agent.objects.all()
    serializer_class = AgentListSerializer


class AgentDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление агента
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    lookup_field = "id"


class PayoutListCreateAPIView(generics.ListCreateAPIView):
    """
    Список и добавление возможных выплат по категориям
    """
    queryset = Payout.objects.all()

    def get_serializer_class(self):
        if self.request.method =="GET":
            return PayoutListSerializer
        elif self.request.method == "POST":
            return PayoutSerializer


class PayoutUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Обновление информации, её просмотр и удаление конкретной выплаты
    """
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    lookup_field = "id"


class InsuranceContractListCreateAPIView(generics.ListCreateAPIView):
    """
    Список и добавление страховых договоров
    """
    queryset = InsuranceContract.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InsuranceContractListSerializer
        elif self.request.method == "POST":
            return InsuranceContractSerializer


class InsuranceContractUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Взаимодействие с отдельным страховым договором
    """
    queryset = InsuranceContract.objects.all()
    serializer_class = InsuranceContractSerializer
    lookup_field = "id"


class InsuranceClaimListCreateAPIView(generics.ListCreateAPIView):
    """
    Выплаты по страховым случаям
    """
    queryset = InsuranceClaim.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InsuranceClaimListSerializer
        elif self.request.method == "POST":
            return InsuranceClaimSerializer


class InsuranceClaimUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Изменение, просмотр, удаление конкретной выплаты по страховому случаю
    """
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer
    lookup_field = "id"


class ActiveAgentsListView(generics.ListAPIView):
    """
    Список активных агентов на данный момент
    """
    serializer_class = AgentListSerializer

    def get_queryset(self):
        return Agent.objects.filter(contract__start_date__lte=timezone.now(),
                                    contract__end_date__gte=timezone.now())


class EnterpriseContractsListView(generics.ListAPIView):
    """
    Список страховых договоров по конкретной компании
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        enterprise_id = self.kwargs['id']
        return InsuranceContract.objects.filter(enterprise_id=enterprise_id)


class AgentContractsListView(generics.ListAPIView):
    """
    Список страховых договоров, заключенных конкретным агентом
    """
    serializer_class = AgentListSerializer

    def get_queryset(self):
        agent_id = self.kwargs['id']
        return InsuranceContract.objects.filter(agent_id=agent_id)


class EnterpriseInsuranceClaimsListView(generics.ListAPIView):
    """
    Выплаты по страховым случаям по конкретной компании
    """
    serializer_class = InsuranceClaimSerializer

    def get_queryset(self):
        enterprise_id = self.kwargs['id']
        return InsuranceClaim.objects.filter(insurance_contract__enterprise_id=enterprise_id)


class SpecializationContractsListView(generics.ListAPIView):
    """
    Страховые договоры с компаниями определенной специализации
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        specialization_id = self.kwargs['id']
        return InsuranceContract.objects.filter(enterprise__specialization_id=specialization_id)


class ClientContractsListView(generics.ListAPIView):
    """
    Список страховых договоров, в которых участвует конкретный пользователь
    """
    serializer_class = InsuranceContractSerializer

    def get_queryset(self):
        client_id = self.kwargs['id']
        return InsuranceContract.objects.filter(clients__id=client_id)


class InsurancePaymentSumView(APIView):
    def get_company_payment(self, request, company_id):
        payments = InsuranceClaim.objects.filter(insurance_contract__enterprise__id=company_id, decision=True)
        total = payments.aggregate(Sum('payout_amount'))['payout_amount__sum'] or 0
        return Response({'total': total})

    def get_agent_payment(self, request, agent_id):
        payments = InsuranceClaim.objects.filter(insurance_contract__agent__id=agent_id, decision=True)
        total = payments.aggregate(Sum('payout_amount'))['payout_amount__sum'] or 0
        return Response({'total': total})


    def get(self, request):
        company_id = request.query_params.get('company_id')
        agent_id = request.query_params.get('agent_id')

        if company_id:
            return self.get_company_payment(request, company_id)
        elif agent_id:
            return self.get_agent_payment(request, agent_id)
        else:
            return Response({'error': 'Specify either company_id or agent_id'})

