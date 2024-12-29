from django.contrib import admin
from django.urls import path, include

from .views.views import IndexView, CVView, ApplicationView
from .views.vacancy_views import VacancyView, VacancyDetailView

urlpatterns = [
    path('', IndexView.as_view()),

    path('cvs/', CVView.as_view(), name='cv-list-view'),

    path('applications/', ApplicationView.as_view(), name='application-list-view'),

    path('vacancies/', VacancyView.as_view(), name='vacancy-list-view'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy-detail'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("admin/", admin.site.urls),
]
