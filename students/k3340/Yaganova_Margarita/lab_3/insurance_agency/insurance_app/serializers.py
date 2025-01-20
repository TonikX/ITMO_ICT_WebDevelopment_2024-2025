from rest_framework import serializers
from .models import *


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class EnterpriseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ["short_name"]


class EmploymentContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentContract
        fields = "__all__"


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class AgentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["username"]


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'


class PayoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['risk_category', 'insured_event']


class InsuranceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceContract
        fields = "__all__"


class InsuranceContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceContract
        fields = ['agent', 'enterprise']


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = "__all__"


class InsuranceClaimListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = ['insurance_contract', 'decision']
