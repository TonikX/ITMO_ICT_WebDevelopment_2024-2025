from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import AircraftList, AircraftDetail, FlightList, FlightDetail, CrewMemberList, CrewMemberDetail, \
    EmployeeList, EmployeeDetail, CustomUserViewSet
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet

urlpatterns = [
    path('api/aircrafts/', AircraftList.as_view(), name='aircraft-list'),
    path('api/aircrafts/<int:pk>/', AircraftDetail.as_view(), name='aircraft-detail'),

    path('api/flights/', FlightList.as_view(), name='flight-list'),
    path('api/flights/<int:pk>/', FlightDetail.as_view(), name='flight-detail'),

    path('api/crew-members/', CrewMemberList.as_view(), name='crew-member-list'),
    path('api/crew-members/<int:pk>/', CrewMemberDetail.as_view(), name='crew-member-detail'),

    path('api/employees/', EmployeeList.as_view(), name='employee-list'),
    path('api/employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),

    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('auth/login/', obtain_auth_token, name='token-create'),
    path('auth/logout/', TokenDestroyView.as_view(), name='token-destroy'),

    path('auth/profile/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='user-profile'),
    path('auth/profile/<int:user_id>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='user-profile'),


]
