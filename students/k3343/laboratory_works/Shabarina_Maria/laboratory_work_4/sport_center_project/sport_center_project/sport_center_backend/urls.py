from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('api/register/', UserRegisterView.as_view(), name='user_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sections/', SectionsListView.as_view(), name='all_sections'),
    path('sportsmen/', SportsmenListView.as_view(), name='all_sportsmen'),
    path('coaches/', CoachesListView.as_view(), name='all_coaches'),
    path('sport_halls/', SportHallsListView.as_view(), name='all_sport_halls'),
    path('schedule/', ScheduleListView.as_view(), name='get_schedule'),
    path('sportsmen/<int:pk>/update/', UpdateSportsmanView.as_view(), name='update_sportsman'),
    path('sections/<int:pk>/', SectionDetailsView.as_view(), name='section_details'),
    path('sections/<int:section_id>/coaches/', CoachesBySectionView.as_view(), name='coaches_by_section'),
    path('sections/<int:section_id>/add_sportsman/', AddSportsmanToSection.as_view(), name='add_sportsman_to_section'),
    path('coaches/<int:coach_id>/report/', generate_report, name='generate_report'),
]