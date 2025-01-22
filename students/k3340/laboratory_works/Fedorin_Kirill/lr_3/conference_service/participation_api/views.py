from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import Participation, ParticipationCreateSerializer, ParticipationDetailedSerializer, ParticipationSerializer, ParticipationUpdateSerializer


class ParticipationAPIView(generics.RetrieveAPIView):
    serializer_class = ParticipationDetailedSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Participation.objects.all()


class ParticipationListAPIView(generics.ListAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Participation.objects.all()

class ParticipationConferenceListAPIView(generics.ListAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        conference_id = self.kwargs['conference_id']
        return Participation.objects.filter(Q(conference__pk=conference_id) & Q(is_cancelled=False))


class ParticipationCreateAPIView(generics.CreateAPIView):
    serializer_class = ParticipationCreateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Participation.objects.all()


class ParticipationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ParticipationUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Participation.objects.all()


class ParticipationDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Participation.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.conference.free_places += 1
        instance.conference.save()
        return super().delete(request, *args, **kwargs)
