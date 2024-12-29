from django.urls import path
from .views import *


app_name = "warriors_app"
urlpatterns = [
    path('sportsmen/', SportsmenAPIView.as_view()),
    path('sportsmen/create', SportsmanCreateView.as_view()),
    path('sportsmen/update/<int:pk>/', SportsmenUpdateView.as_view()),
    path('sportsmen/delete/<int:pk>/', SportsmenDeleteView.as_view()),
    path('sports/', SportAPIView.as_view()),
    path('sports/create', SportCreateView.as_view()),
    path('coaches/', CoachAPIView.as_view()),
    path('coaches/create', CoachCreateView.as_view()),
    path('coaches/update/<int:pk>/', CoachUpdateView.as_view()),
    path('coaches/delete/<int:pk>/', CoachDeleteView.as_view()),
    path('equipment/', EquipmentAPIView.as_view()),
    path('equipment/create', EquipmentCreateView.as_view()),
    path('sport_halls/', SportHallAPIView.as_view()),
    path('sport_halls/create', SportHallCreateView.as_view()),
    path('sport_halls_equipment/', EquipmentOfSportHallAPIView.as_view()),
    path('sport_halls_equipment/create', EquipmentOfSportHallCreateView.as_view()),
    path('sport_halls_equipment/update/<int:pk>/', EquipmentOfSportHallUpdateView.as_view()),
    path('sport_sections/', SportSectionAPIView.as_view()),
    path('sport_sections/create', SportSectionCreateView.as_view()),
    path('sport_sections/update/<int:pk>/', SportSectionUpdateView.as_view()),
    path('sport_sections/delete/<int:pk>/', SportSectionDeleteView.as_view()),
    path('schedule/', ScheduleAPIView.as_view()),
    path('schedule/create', ScheduleCreateView.as_view()),
    path('schedule/update/<int:pk>/', ScheduleUpdateView.as_view()),
    path('schedule/delete/<int:pk>/', ScheduleDeleteView.as_view()),
    path('sport_sections_coaches/', SportSectionCoachesView.as_view()),
    path('sport_sections_coaches/create', SportSectionCoachesCreateView.as_view()),
    path('sport_sections_coaches/update/<int:pk>/', SportSectionCoachesUpdateView.as_view()),
    path('sport_sections_coaches/update/<int:pk>/', SportSectionCoachesDeleteView.as_view()),

    path('sport_sections/search', SportSectionSearchAPIView.as_view()),
    path('sport_section_sportsmen/', SportSectionSportsmenSearchAPIView.as_view()),
    path('coach_schedule/', CoachScheduleSearchAPIView.as_view()),
    path('sport_hall_equipment/', SportHallEquipmentSearchAPIView.as_view()),
    path('sections_by_sport/', SectionsBySportSearchAPIView.as_view()),
]