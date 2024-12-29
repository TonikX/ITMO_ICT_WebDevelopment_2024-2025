from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hh.models import CV, Application
from hh.permissions import IsJobSeeker
from hh.serializers import CVSerializer, ApplicantSerializer


class IndexView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user must be authenticated

    def get(self, request):
        return Response({'message': 'you are logged in'})


class CVView(ListCreateAPIView):
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return CV.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApplicationView(ListCreateAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return Application.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
