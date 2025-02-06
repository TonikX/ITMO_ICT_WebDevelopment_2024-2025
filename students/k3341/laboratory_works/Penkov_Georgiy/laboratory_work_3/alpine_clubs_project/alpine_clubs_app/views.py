from rest_framework.permissions import SAFE_METHODS
from rest_framework import generics
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from alpine_clubs_app.models import (
    Club,
    City,
    Country,
    Mountain,
    Route,
    Ascent,
    AscentParticipation,
    ClubMembership,
)
from alpine_clubs_app.serializers import (
    ClubSerializer,
    CitySerializer,
    CityDetailSerializer,
    CountrySerializer,
    CountryDetailSerializer,
    MountainSerializer,
    MountainDetailSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    AscentSerializer,
    AscentDetailSerializer,
    AscentParticipationSerializer,
    ClubDetailSerializer,
    ClubMembershipSerializer,
    MyClubMemberShipSerializer,
    MyAscentParticipationSerializer,
)
from alpine_clubs_app.permissions import IsAdminOrReadOnly
from alpine_clubs_app.filters import ClubMembershipFilter
from django.contrib.auth import get_user_model

User = get_user_model()


class CityListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["country"]
    ordering_fields = ["id", "name", "country__name"]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CityDetailSerializer
        return CitySerializer


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CityDetailSerializer
        return CitySerializer


class CountryListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "name"]


class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CountryDetailSerializer
    queryset = Country.objects.all()


class MountainListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MountainSerializer
    queryset = Mountain.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["country"]
    ordering_fields = ["id", "name", "elevation"]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MountainDetailSerializer
        return MountainSerializer


class MountainDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MountainDetailSerializer
    queryset = Mountain.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MountainDetailSerializer
        return MountainSerializer


class RouteListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["mountain"]
    ordering_fields = ["id", "name", "duration_days"]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RouteDetailSerializer
        return RouteSerializer


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = RouteDetailSerializer
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RouteDetailSerializer
        return RouteSerializer


class AscentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AscentSerializer
    queryset = Ascent.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["route__mountain", "route"]
    ordering_fields = ["id", "planned_start_datetime"]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AscentDetailSerializer
        return AscentSerializer


class MyAscentParticipationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyAscentParticipationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["ascent__route__mountain"]
    ordering_fields = ["id", "ascent__planned_start_datetime"]

    def get_queryset(self):
        user = self.request.user
        ascent_participations = AscentParticipation.objects.filter(user=user).order_by(
            "-ascent__planned_start_datetime"
        )
        return ascent_participations


class AscentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AscentSerializer
    queryset = Ascent.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AscentDetailSerializer
        return AscentSerializer


class AscentParticipationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AscentParticipationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_successful", "incident_type"]

    def get_queryset(self):
        ascent_pk = self.kwargs["pk"]
        ascent = generics.get_object_or_404(Ascent, id=ascent_pk)
        return AscentParticipation.objects.filter(ascent=ascent)

    def perform_create(self, serializer):
        user = self.request.user
        ascent_pk = self.kwargs["pk"]
        ascent = generics.get_object_or_404(Ascent, id=ascent_pk)
        if AscentParticipation.objects.filter(user=user, ascent=ascent).exists():
            raise serializers.ValidationError(
                "User is already participating in this ascent."
            )
        serializer.save(user=user, ascent=ascent)


class AscentParticipationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AscentParticipationSerializer

    def get_object(self):
        return generics.get_object_or_404(
            AscentParticipation,
            id=self.kwargs["ascentparticipation_pk"],
            ascent__pk=self.kwargs["ascent_pk"],
        )


class ClubListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["country"]
    ordering_fields = ["id", "name"]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ClubDetailSerializer
        return ClubSerializer


class ClubDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ClubSerializer
    queryset = Club.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ClubDetailSerializer
        return ClubSerializer


class ClubMembershipListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ClubMembershipSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClubMembershipFilter
    ordering_fields = ["id", "join_datetime"]

    def get_queryset(self):
        club_pk = self.kwargs["pk"]
        club = generics.get_object_or_404(Club, id=club_pk)
        return ClubMembership.objects.filter(club=club)

    def perform_create(self, serializer):
        user = self.request.user
        club_pk = self.kwargs["pk"]
        club = generics.get_object_or_404(Club, id=club_pk)
        if ClubMembership.objects.filter(
            user=user, club=club, leave_datetime__isnull=True
        ).exists():
            raise serializers.ValidationError("User is already a member in this club.")
        if ClubMembership.objects.filter(
            user=user, leave_datetime__isnull=True
        ).exists():
            raise exceptions.ValidationError(
                "User is already a member in other club. To join, leave other club."
            )
        serializer.save(user=user, club=club)


class ClubMembershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ClubMembershipSerializer

    def get_object(self):
        return generics.get_object_or_404(
            ClubMembership,
            id=self.kwargs["membership_pk"],
            club__pk=self.kwargs["club_pk"],
        )


class ClubMembershipLeaveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClubMembershipSerializer

    def get_object(self):
        return generics.get_object_or_404(
            ClubMembership,
            user=self.request.user,
            club__pk=self.kwargs["pk"],
            leave_datetime__isnull=True,
        )

    def perform_update(self, serializer):
        serializer.validated_data["leave_datetime"] = timezone.now()
        serializer.save()


class MyClubMembershipListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyClubMemberShipSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClubMembershipFilter
    ordering_fields = ["id", "join_datetime"]

    def get_queryset(self):
        user = self.request.user
        club_memberships = ClubMembership.objects.filter(user=user).order_by(
            "-join_datetime"
        )
        return club_memberships
