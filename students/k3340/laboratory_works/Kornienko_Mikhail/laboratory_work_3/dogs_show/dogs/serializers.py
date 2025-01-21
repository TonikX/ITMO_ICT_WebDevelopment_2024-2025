from rest_framework import serializers
from drf_yasg import openapi
from .models import Owner, Dog, Show, Participation, Expert, Grade

class UUIDPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_schema_field(self, view):
        example = None
        try:
            example_instance = self.get_queryset().first()
            if example_instance:
                example = str(example_instance.pk)
        except:
            pass
        if not example:
            example = '00000000-0000-0000-0000-000000000000'
        return openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID,
            title=self.label or 'UUID',
            description=self.help_text or 'UUID of the related object',
            example=example
        )


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class DogSerializer(serializers.ModelSerializer):
    owner_id = UUIDPrimaryKeyRelatedField(queryset=Owner.objects.all(), source='owner')
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Dog
        fields = '__all__'


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'


class ParticipationSerializer(serializers.ModelSerializer):
    dog_id = UUIDPrimaryKeyRelatedField(queryset=Dog.objects.all(), source='dog')
    dog = DogSerializer(read_only=True)
    show_id = UUIDPrimaryKeyRelatedField(queryset=Show.objects.all(), source='show')
    show = ShowSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    participation_id = UUIDPrimaryKeyRelatedField(
        queryset=Participation.objects.all(),
        source='participation',
    )
    participation = ParticipationSerializer(read_only=True)
    expert_id = UUIDPrimaryKeyRelatedField(
        queryset=Expert.objects.all(),
        source='expert'
    )
    expert = ExpertSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'
