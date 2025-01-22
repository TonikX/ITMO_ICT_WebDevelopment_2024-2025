from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from conference_api.serializers import ConferenceSerializer
from conference_api.models import Conference
from participation_api.models import Participation
from participation_api.serializers import ParticipationSerializer
from work_api.models import Employee
from work_api.serializers import EmployeeSerializer

from .models import UserAccount
from .serializers import CustomUserSerializer, UserSerializerParticipation, UserUpdateSerializer


class UserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializerParticipation
    lookup_field = 'id'
    queryset = UserAccount.objects.all()

class UserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserAccount.objects.all()

class ClientsFromTownListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        town = self.kwargs.get('from_town')
        return UserAccount.objects.filter(participation__from_town=town)


class UserRelatedReviewersListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        date = self.kwargs['date']
        return Employee.objects.filter(Q(contracts__work_schedule__date=date) & Q(contracts__work_schedule__participation__client__pk=self.kwargs['id']))


class UserParticipationListAPIView(generics.ListAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Participation.objects.filter(client__pk=self.kwargs['id'])


class UsersRegistrationsListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        start_date = self.kwargs.get('from')
        end_date = self.kwargs.get('to')
        query = Q()
        if start_date:
            query &= Q(participation__registration_date__gte=start_date)
        if end_date:
            query &= Q(participation__registration_date__lte=end_date)
        return UserAccount.objects.filter(query)

class UserConferencesListAPIView(generics.ListAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Conference.objects.filter(participation__client__pk=self.kwargs['id'])

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'id'
    queryset = UserAccount.objects.all()
