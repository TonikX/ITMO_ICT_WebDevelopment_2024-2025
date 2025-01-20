from rest_framework import serializers
from .models import (InsuranceAgent, Organization, Employee, CollectiveContract,
                     InsuranceCase, EmploymentContract)

class InsuranceAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceAgent
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class CollectiveContractSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)
    class Meta:
        model = CollectiveContract
        fields = '__all__'

class InsuranceCaseSerializer(serializers.ModelSerializer):
    contract = CollectiveContractSerializer()
    class Meta:
        model = InsuranceCase
        fields = '__all__'

class EmploymentContractSerializer(serializers.ModelSerializer):
    insurance_agent = InsuranceAgentSerializer(read_only=True)
    class Meta:
        model = EmploymentContract
        fields = '__all__'
