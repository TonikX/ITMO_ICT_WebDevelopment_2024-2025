from django.urls import path

from .views import (
    ParticipationAPIView,
    ParticipationConferenceListAPIView,
    ParticipationCreateAPIView,
    ParticipationDeleteAPIView,
    ParticipationListAPIView,
    ParticipationUpdateAPIView,
)

app_name = "participation_api"

urlpatterns = [
    path('participation/<int:id>/', ParticipationAPIView.as_view(), name='get_participation'),
    path('participation/list/', ParticipationListAPIView.as_view(), name='get_participation_list'),
    path('participation/add/', ParticipationCreateAPIView.as_view(), name='add_participation'),
    path('participation/<int:id>/update/', ParticipationUpdateAPIView.as_view(), name='update_participation'),
    path('participation/<int:id>/delete/', ParticipationDeleteAPIView.as_view(), name='delete_participation'),
    path('participation/conference/<int:conference_id>/', ParticipationConferenceListAPIView.as_view(), name='get_participation_by_conference'),
]