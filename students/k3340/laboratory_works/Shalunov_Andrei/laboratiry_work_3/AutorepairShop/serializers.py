from rest_framework import serializers
from .models import (
    User, Client, Employee, CarWorkshop,
    JobPosition, Automobile, Model, Contract,
    Service, Detail, CarDetail, DetailsFromClient,
    DistributionOfWork, DetailInService,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
        ref_name = "AutorepairShopUser"


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Client
        fields = ['id', 'user', 'user_id', 'full_name', 'phone', 'email']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    job_position = serializers.PrimaryKeyRelatedField(queryset=JobPosition.objects.all())
    car_workshop = serializers.PrimaryKeyRelatedField(queryset=CarWorkshop.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'user', 'user_id', 'full_name', 'phone', 'email', 'job_position', 'car_workshop', 'rank', 'bonus']


class CarWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarWorkshop
        fields = ['id', 'address', 'city']


class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = ['id', 'name', 'specialisation', 'salary']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'car_brand', 'country_of_production', 'model', 'car_power']


class AutomobileSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    auto_model = ModelSerializer(read_only=True)
    auto_model_id = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.all(), source='auto_model', write_only=True
    )

    class Meta:
        model = Automobile
        fields = ['id', 'engine_number', 'year_of_vehicle', 'colour', 'state_number', 'client', 'client_id', 'auto_model', 'auto_model_id']


class ContractSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    auto = AutomobileSerializer(read_only=True)
    auto_id = serializers.PrimaryKeyRelatedField(
        queryset=Automobile.objects.all(), source='auto', write_only=True
    )
    employee = EmployeeSerializer(read_only=True)  # Поле для чтения данных о сотруднике
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = Contract
        fields = [
            'id', 'order_date', 'order_status', 'payment_status', 'date_of_acceptance_for_repair',
            'scheduled_date_end_of_repair', 'actual_date_end_of_repair', 'total_payment',
            'client', 'client_id', 'auto', 'auto_id', 'employee', 'employee_id'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'type_of_repair', 'category_repair', 'price']


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'name', 'price', 'country_of_manufacturer']


class CarDetailSerializer(serializers.ModelSerializer):
    automobile = AutomobileSerializer(read_only=True)
    automobile_id = serializers.PrimaryKeyRelatedField(
        queryset=Automobile.objects.all(), source='automobile', write_only=True
    )
    detail = DetailSerializer(read_only=True)
    detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Detail.objects.all(), source='detail', write_only=True
    )

    class Meta:
        model = CarDetail
        fields = ['id', 'automobile', 'automobile_id', 'detail', 'detail_id']


class DistributionOfWorkSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )
    contract = ContractSerializer(read_only=True)
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True
    )

    class Meta:
        model = DistributionOfWork
        fields = ['id', 'status', 'start_date', 'scheduled_end_date', 'actual_end_date',
                  'service', 'service_id', 'contract', 'contract_id', 'quantity_of_services']


class DetailsFromClientSerializer(serializers.ModelSerializer):
    detail = DetailSerializer(read_only=True)
    detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Detail.objects.all(), source='detail', write_only=True
    )
    distribution = DistributionOfWorkSerializer(read_only=True)
    distribution_id = serializers.PrimaryKeyRelatedField(
        queryset=DistributionOfWork.objects.all(), source='distribution', write_only=True, allow_null=True
    )

    class Meta:
        model = DetailsFromClient
        fields = ['id', 'detail', 'detail_id', 'distribution', 'distribution_id', 'amount_of_detail', 'supplier']


class DetailInServiceSerializer(serializers.ModelSerializer):
    detail = DetailSerializer(read_only=True)
    detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Detail.objects.all(), source='detail', write_only=True
    )
    contract = ContractSerializer(read_only=True)
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True
    )

    class Meta:
        model = DetailInService
        fields = ['id', 'detail', 'detail_id', 'contract', 'contract_id', 'number_of_details']
