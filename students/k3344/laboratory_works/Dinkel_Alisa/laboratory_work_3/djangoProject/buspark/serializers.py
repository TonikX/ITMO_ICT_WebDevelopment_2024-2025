from rest_framework import serializers
from .models import BusCategory, Bus, Driver, Route, Shift


class BusCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCategory
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    capacity = serializers.ReadOnlyField()  # Вместимость рассчитывается автоматически

    class Meta:
        model = Bus
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    salary = serializers.ReadOnlyField()  # Оклад рассчитывается динамически

    class Meta:
        model = Driver
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    # driver = DriverSerializer()
    # bus = BusSerializer()
    # route = RouteSerializer()

    class Meta:
        model = Shift
        fields = "__all__"

    def validate(self, data):
        """Валидация логики при создании смены"""

        shift_date = data["shift_date"]
        start_time = data["start_time"]
        end_time = data["end_time"]
        bus = data.get("bus")
        driver = data.get("driver")
        status = data.get("status")

        # Проверяем, что водитель не активен в двух сменах одновременно
        if driver and status == "Active":
            overlapping_driver_shifts = Shift.objects.filter(
                shift_date=shift_date,
                driver=driver,
                status="Active",  # Только активные смены
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_driver_shifts.exists():
                raise serializers.ValidationError("Этот водитель уже работает в другой активной смене в это время.")

        # Проверяем, что автобус не активен в двух сменах одновременно
        if bus and status == "Active":
            overlapping_bus_shifts = Shift.objects.filter(
                shift_date=shift_date,
                bus=bus,
                status="Active",  # Только активные смены
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_bus_shifts.exists():
                raise serializers.ValidationError(
                    "Этот автобус уже используется в другой активной смене в это время.")

        # Автобус с Breakdown не может быть активным в другой смене
        if bus and status == "Active":
            overlapping_bus_shifts = Shift.objects.filter(
                shift_date=shift_date,
                bus=bus,
                status="Breakdown",
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_bus_shifts.exists():
                raise serializers.ValidationError("Сломанный автобус не может быть активным в другой смене в это время.")

        # Водитель с No Driver не может быть активным в другой смене
        if driver and status == "Active":
            overlapping_driver_shifts = Shift.objects.filter(
                shift_date=shift_date,
                bus=bus,
                status="No Driver",
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_driver_shifts.exists():
                raise serializers.ValidationError(
                    "Отсутствующий водитель не может быть активным в другой смене в это время.")

        return data
