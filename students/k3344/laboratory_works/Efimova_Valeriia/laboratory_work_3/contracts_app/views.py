from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from contracts_app.models import *
from contracts_app.permissions import IsAdminOrReadOnly
from contracts_app.serializers import *


def home(request):
    return render(request, "home.html")


def register(request):
    return render(request, "register.html")


def login(request):
    return render(request, "login.html")


def profile(request):
    return render(request, "profile.html")


class AgentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAdminOrReadOnly]


class AgentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrganizationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrganizationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContractListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContractDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAdminOrReadOnly]


class InsuranceCaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer
    permission_classes = [IsAdminOrReadOnly]


class InsuranceCaseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer
    permission_classes = [IsAdminOrReadOnly]


class EmploymentContractListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
    permission_classes = [IsAdminOrReadOnly]


class EmploymentContractDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContractReportView(APIView):
    def get(self, request, pk):
        try:
            contract = Contract.objects.get(pk=pk)
            serializer = ContractReportSerializer(contract)
            return Response(serializer.data)
        except Contract.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
