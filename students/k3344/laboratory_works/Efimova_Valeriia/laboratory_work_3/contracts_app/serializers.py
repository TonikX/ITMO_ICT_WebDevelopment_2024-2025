from rest_framework import serializers
from .models import *


class AgentSerializer(serializers.ModelSerializer):
    employment_contract_id = serializers.SerializerMethodField()
    contract_ids = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            "id",
            "full_name",
            "passport_details",
            "contact_details",
            "employment_contract_id",
            "contract_ids",
        ]

    def get_employment_contract_id(self, obj):
        contract = obj.employment_contracts.order_by("-start_date").first()
        return contract.id if contract else None

    def get_contract_ids(self, obj):
        return [contract.id for contract in obj.contracts.all()]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), write_only=True, source="organization"
    )

    class Meta:
        model = Employee
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), write_only=True, source="organization"
    )
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), write_only=True, source="agent"
    )
    employees = EmployeeSerializer(many=True, read_only=True)
    employees_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True, source="employees", many=True
    )

    class Meta:
        model = Contract
        fields = "__all__"


class InsuranceCaseSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(read_only=True)
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), write_only=True, source="contract"
    )

    class Meta:
        model = InsuranceCase
        fields = "__all__"


class EmploymentContractSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), write_only=True, source="agent"
    )

    class Meta:
        model = EmploymentContract
        fields = "__all__"


class InsuranceCaseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCase
        fields = ["date", "cause", "decision", "amount"]


class ContractReportSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    cases = InsuranceCaseShortSerializer(many=True, read_only=True)
    total_payout = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            "id",
            "contract_type",
            "organization",
            "agent",
            "start_date",
            "end_date",
            "insurance_cost",
            "cases",
            "total_payout",
        ]

    def get_total_payout(self, obj):
        total = sum(case.amount for case in obj.cases.all() if case.decision)
        return total
