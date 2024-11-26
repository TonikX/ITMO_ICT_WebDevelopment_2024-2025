from rest_framework import serializers
from .models import (
    InsuranceAgency, Agent, EmploymentContract, Organization,
    Employee, Position, Contract, InsuranceCase
)

class InsuranceAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceAgency
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class EmploymentContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentContract
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class InsuranceCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCase
        fields = '__all__'
