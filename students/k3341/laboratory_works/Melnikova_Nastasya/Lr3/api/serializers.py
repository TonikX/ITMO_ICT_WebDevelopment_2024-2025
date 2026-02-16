from rest_framework import serializers
from .models import Room, Guest, Stay, Staff, CleaningSchedule


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'

    def validate(self, data):
        room = data.get('room')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if check_in >= check_out:
            raise serializers.ValidationError("check_out must be after check_in")

        overlapping_stays = Stay.objects.filter(
            room=room
        ).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        )

        if self.instance:
            overlapping_stays = overlapping_stays.exclude(id=self.instance.id)

        if overlapping_stays.exists():
            raise serializers.ValidationError("Номер уже занят в этот период 😎")

        return data





class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'
