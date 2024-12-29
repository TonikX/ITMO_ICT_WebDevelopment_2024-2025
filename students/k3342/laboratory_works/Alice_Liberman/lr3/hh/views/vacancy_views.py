from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from hh.models import Vacancy, Application
from hh.permissions import IsHR
from hh.serializers import VacancySerializer, VacancyListSerializer, \
    VacancyCreateSerializer, ApplicantSerializer


class VacancyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class VacancyView(ListCreateAPIView):
    serializer_class = VacancyListSerializer
    pagination_class = VacancyPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous or user.role == 'job_seeker':
            return Vacancy.objects.all()

        return Vacancy.objects.filter(company=user.company)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsHR()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VacancyCreateSerializer
        return VacancyListSerializer


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        vacancy_serializer = self.get_serializer(vacancy)

        if request.user.role == 'hr':
            applications = Application.objects.filter(vacancy=vacancy)

            applications_serializer = ApplicantSerializer(applications, many=True)

            return Response({
                'vacancy': vacancy_serializer.data,
                'applications': applications_serializer.data
            })

        return Response(vacancy_serializer.data)

