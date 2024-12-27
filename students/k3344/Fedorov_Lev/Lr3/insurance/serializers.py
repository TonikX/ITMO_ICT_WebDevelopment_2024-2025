from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (InsuranceAgency, Agent, EmploymentContract, Organization, Employee,
                     Position, Contract, InsuranceCase, CustomUser)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'code', 'full_name', 'short_name', 'address', 'bank_details', 'specialization']

class EmploymentContractSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())

    class Meta:
        model = EmploymentContract
        fields = ['id', 'agent', 'organization', 'start_date', 'end_date', 'salary']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'is_staff']

class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    organization = OrganizationSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'age', 'risk_category', 'payout_amount', 'position', 'passport_data', 'organization']

class AgentSerializer(serializers.ModelSerializer):
    contracts = EmploymentContractSerializer(many=True, read_only=True, source='employment_contracts')

    class Meta:
        model = Agent
        fields = ['id', 'first_name', 'last_name', 'passport_data', 'contact_info', 'contracts']

class ContractSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    organization = OrganizationSerializer()
    employees = EmployeeSerializer(many=True)

    class Meta:
        model = Contract
        fields = ['id', 'agent', 'organization', 'employees', 'start_date', 'end_date', 'total_sum', 'contract_type', 'contract_info']

class InsuranceCaseSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()

    class Meta:
        model = InsuranceCase
        fields = ['id', 'contract', 'date', 'reason', 'payout_decision', 'payout_amount']

class CustomUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'organization']

class InsuranceAgencySerializer(serializers.ModelSerializer):
    agents = AgentSerializer(many=True)

    class Meta:
        model = InsuranceAgency
        fields = ['id', 'name', 'agents', 'agency_info']

class EmploymentContractDetailedSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    agency = InsuranceAgencySerializer()

    class Meta:
        model = EmploymentContract
        fields = ['id', 'agent', 'agency', 'start_date', 'end_date', 'salary']

class AgentContractStatsSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    total_contracts = serializers.IntegerField()
    total_salary = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        fields = ['agent_id', 'total_contracts', 'total_salary']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user