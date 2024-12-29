from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now
from rest_framework import serializers

from .models import (InsuranceAgency, Agent, EmploymentContract, Organization, Employee,
                     Position, Contract, InsuranceCase, CustomUser)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'code', 'full_name', 'short_name', 'address', 'bank_details', 'specialization']


class EmploymentContractSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
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
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'age', 'risk_category', 'payout_amount', 'position', 'passport_data',
                  'organization']

    def validate_passport_data(self, value):
        if Employee.objects.filter(passport_data=value).exists():
            raise serializers.ValidationError("Employee with this passport already exists.")
        return value

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Employee must be at least 18 years old.")
        return value

    def update(self, instance, validated_data):
        position_data = validated_data.pop('position', None)
        if position_data:
            position_serializer = PositionSerializer(instance.position, data=position_data)
            position_serializer.is_valid(raise_exception=True)
            position_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AgentSerializer(serializers.ModelSerializer):
    contracts = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='employment_contracts')

    class Meta:
        model = Agent
        fields = ['id', 'first_name', 'last_name', 'passport_data', 'contact_info', 'contracts']


class ContractSerializer(serializers.ModelSerializer):
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    employees = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True)

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

    class Meta:
        model = Contract
        fields = ['id', 'agent', 'organization', 'employees', 'start_date', 'end_date', 'total_sum', 'contract_type',
                  'contract_info', 'status']

    def create(self, validated_data):
        validated_data['start_date'] = now().date()  # Устанавливаем текущую дату
        return super().create(validated_data)


class InsuranceCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCase
        fields = ['id', 'contract', 'date', 'reason', 'payout_amount', 'status', 'payout_decision']

    def validate(self, data):
        # Если кейс одобрен или отклонен, необходимо указать решение
        if data.get('status') in ['approved', 'rejected']:
            if not data.get('payout_decision'):
                raise serializers.ValidationError({
                    'payout_decision': 'This field is required when approving or rejecting a case.'
                })

        # Если статус "approved", сумма выплаты не может быть пустой или равной 0
        if data.get('status') == 'approved' and not data.get('payout_amount'):
            raise serializers.ValidationError({
                'payout_amount': 'Payout amount is required when approving a case.'
            })

        return data

    def create(self, validated_data):
        # Устанавливаем payout_amount и payout_decision как пустые, если сотрудник создает кейс
        validated_data['payout_amount'] = None
        validated_data['payout_decision'] = None
        validated_data['status'] = 'pending'  # Статус по умолчанию
        return super().create(validated_data)




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
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )
    agency = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceAgency.objects.all(), required=False, allow_null=True
    )
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False
    )
    payout_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=0
    )
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'password', 're_password', 'role',
            'organization', 'passport_data', 'position', 'agency', 'payout_amount'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Валидация паролей
        if data['password'] != data.pop('re_password', None):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        # Убираем лишние поля перед созданием пользователя
        position = validated_data.pop('position', None)
        agency = validated_data.pop('agency', None)
        payout_amount = validated_data.pop('payout_amount', 0)

        # Создаем пользователя
        user = CustomUser.objects.create_user(**validated_data)

        # Если регистрируем сотрудника
        if validated_data['role'] == 'employee':
            Employee.objects.create(
                user=user,
                position=position,
                organization=validated_data.get('organization'),
                first_name=user.username,
                last_name='-',
                passport_data=validated_data.get('passport_data'),
                age=validated_data.get('age', 18),
            )

        # Если регистрируем агента
        elif validated_data['role'] == 'agent':
            agent = Agent.objects.create(
                user=user,
                first_name=user.username,
                last_name='-',
                passport_data=validated_data.get('passport_data')
            )
            # Привязка агента к агентству после создания
            if agency:
                agency.agents.add(agent)

        return user


class AgentRegisterSerializer(RegisterSerializer):
    def create(self, validated_data):
        validated_data['role'] = 'agent'
        return super().create(validated_data)


class EmployeeRegisterSerializer(RegisterSerializer):
    def create(self, validated_data):
        validated_data['role'] = 'employee'
        return super().create(validated_data)


class DirectorRegisterSerializer(RegisterSerializer):
    def create(self, validated_data):
        validated_data['role'] = 'org_admin'
        return super().create(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    re_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['re_password']:
            raise serializers.ValidationError({"re_password": "Passwords do not match"})
        return data