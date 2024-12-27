from django.urls import path
from rest_framework.routers import DefaultRouter

from hotel_app.views import ClientsListView, RoomsByStatusView, ClientStayOverlapView, ClientRoomCleaningView, \
    EmployeeManagementView, CleaningScheduleManagementView, ReservationManagementView, QuarterlyReportView, \
    ClientViewSet, RoomViewSet, ReservationViewSet, EmployeeViewSet, CleaningScheduleViewSet, PublicEndpoint, \
    EmployeePositionsViewSet, EmploymentContractViewSet

urlpatterns = [
    path('clients', ClientsListView.as_view(), name='clients-list'),
    path('rooms', RoomsByStatusView.as_view(), name='available-rooms-count'),
    path('clients/stay-overlap', ClientStayOverlapView.as_view(), name='client-stay-overlap'),
    path('clients/room-cleaner', ClientRoomCleaningView.as_view(), name='client-room-cleaning'),
    path('employees/manage', EmployeeManagementView.as_view(), name='employee-management'),
    path('cleaning-schedules/manage', CleaningScheduleManagementView.as_view(), name='update-cleaning-schedule'),
    path('reservation', ReservationManagementView.as_view(), name='create-reservation'),
    path('reservation/<int:reservation_id>', ReservationManagementView.as_view(), name='update-reservation'),
    path('reports/quarterly', QuarterlyReportView.as_view(), name='quarterly-report'),
    path("health", PublicEndpoint.as_view(), name='hello-world')
]

router = DefaultRouter()
router.register(r'api/clients', ClientViewSet, basename='client')
router.register(r'api/rooms', RoomViewSet, basename='room')
router.register(r'api/reservations', ReservationViewSet, basename='reservation')
router.register(r'api/employees', EmployeeViewSet, basename='employee')
router.register(r'api/employment-contracts', EmploymentContractViewSet, basename='employee-contracts')
router.register(r'api/positions', EmployeePositionsViewSet, basename='employee-position')
router.register(r'api/cleaning-schedules', CleaningScheduleViewSet, basename='cleaning-schedule')

urlpatterns += router.urls