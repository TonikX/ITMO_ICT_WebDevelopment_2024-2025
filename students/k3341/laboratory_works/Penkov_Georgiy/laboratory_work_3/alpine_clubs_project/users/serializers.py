from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from alpine_clubs_app.models import ClubMembership
from alpine_clubs_app.serializers import ClubSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    club = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "phone_number",
            "city",
            "club",
        )

    @extend_schema_field(ClubSerializer)
    def get_club(sef, obj):
        try:
            current_membership = ClubMembership.objects.get(
                user=obj, leave_datetime__isnull=True
            )
            return ClubSerializer(current_membership.club).data
        except ClubMembership.DoesNotExist:
            return None


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number"),
            city=validated_data.get("city"),
        )
        return user
