import datetime

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import Conference, ConferenceSerializer, ConferenceUpdateSerializer


class ConferenceAPIView(generics.RetrieveAPIView):
    serializer_class = ConferenceSerializer
    lookup_field = 'id'
    queryset = Conference.objects.all()


class ConferenceListAPIView(generics.ListAPIView):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()


class ConferenceDateFilteredAPIView(generics.ListAPIView):
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        start_date, end_date = self.kwargs['from'], self.kwargs['to']

        return Conference.objects.filter(
            Q(is_registration_opened=True)
            & Q(free_places__gt=0)
            & Q(start_date__gte=start_date)
            & Q(start_date__lte=end_date),
        )


class OpennedConferencesAPIView(generics.ListAPIView):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.filter(Q(is_registration_opened=True) & Q(free_places__gt=0) & Q(start_date__gt=datetime.date.today()))

class ConferenceUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ConferenceUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = Conference.objects.all()
