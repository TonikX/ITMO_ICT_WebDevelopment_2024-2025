from rest_framework import serializers
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from alpine_clubs_app.models import (
    Club,
    ClubMembership,
    City,
    Country,
    Mountain,
    Route,
    Ascent,
    AscentParticipation,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CountryDetailSerializer(serializers.ModelSerializer):
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    mountains = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    clubs = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Country
        fields = ("id", "name", "cities", "clubs", "mountains")


class CitySerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), allow_null=True
    )

    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "country")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class MountainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mountain
        fields = "__all__"


class MountainDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    routes = RouteSerializer(read_only=True, many=True)

    class Meta:
        model = Mountain
        fields = ("id", "name", "elevation", "region", "country", "routes")


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"

    def validate(self, data):
        city = data.get("city")
        country = data.get("country")

        if city and country:
            raise serializers.ValidationError(
                "Cannot specify both city and country simultaneously."
            )
        if city:
            data["country"] = city.country

        return data


class AscentParticipationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AscentParticipation
        fields = "__all__"
        read_only_fields = ("user", "ascent")

    def get_user(self, obj):
        from users.serializers import UserSerializer

        return UserSerializer(obj.user).data


class AscentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ascent
        fields = "__all__"


class AscentDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    mountain = serializers.SerializerMethodField()
    participants = AscentParticipationSerializer(read_only=True, many=True)

    class Meta:
        model = Ascent
        fields = "__all__"

    @extend_schema_field(MountainSerializer)
    def get_mountain(self, obj):
        return (
            MountainSerializer(obj.route.mountain).data if obj.route.mountain else None
        )


class MyAscentParticipationSerializer(AscentParticipationSerializer):
    ascent = AscentDetailSerializer(read_only=True)


class RouteDetailSerializer(serializers.ModelSerializer):
    mountain = MountainSerializer(read_only=True)
    ascents = AscentSerializer(read_only=True, many=True)

    class Meta:
        model = Route
        fields = ("id", "name", "description", "duration_days", "mountain", "ascents")


class ClubMembershipSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ClubMembership
        fields = "__all__"
        read_only_fields = ("user", "club")

    def get_user(self, obj):
        from users.serializers import UserSerializer

        return UserSerializer(obj.user).data

    def validate(self, data):
        if self.instance:
            join_datetime = data.get("join_datetime", self.instance.join_datetime)
            leave_datetime = data.get("leave_datetime", self.instance.leave_datetime)
        else:
            join_datetime = data.get("join_datetime")
            leave_datetime = data.get("leave_datetime")

        if leave_datetime and join_datetime > leave_datetime:
            raise serializers.ValidationError(
                "Join datetime must be earlier than leave datetime."
            )
        if leave_datetime and leave_datetime > timezone.now():
            raise serializers.ValidationError(
                "Leave datetime must not be from the future."
            )

        return data


class MyClubMemberShipSerializer(ClubMembershipSerializer):
    club = ClubSerializer(read_only=True)


class ClubDetailSerializer(serializers.ModelSerializer):
    members = ClubMembershipSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    contact_user = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = "__all__"

    def get_contact_user(self, obj):
        from users.serializers import UserSerializer

        return UserSerializer(obj.contact_user).data
