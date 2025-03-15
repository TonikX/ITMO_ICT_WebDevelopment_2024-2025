from django.urls import path
from .views import (
    RaceListView, RaceDetailView, RaceRegistrationView, CommentCreateView,
    UserRegistrationView, LogoutUser, RacerProfileCreateView, RacerProfileView,
    RaceUnregisterView, RacerProfileUpdateView, EditRaceView, DeleteRaceView,
    DeleteCommentView, DeleteRacerFromRegistrationView, DeleteRacerFromRaceResultView
)

urlpatterns = [
    path('', RaceListView.as_view(), name='race_list'),
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/logout/', LogoutUser.as_view(), name='logout'),
    path('race/<int:pk>/', RaceDetailView.as_view(), name='race_detail'),
    path('race/<int:race_id>/register', RaceRegistrationView.as_view(), name='register_race'),
    path('race/<int:race_id>/unregister', RaceUnregisterView.as_view(), name='unregister_race'),
    path('race/<int:race_id>/comment', CommentCreateView.as_view(), name='add_comment'),
    path('race/<int:race_id>/comment/<int:pk>/delete/admin', DeleteCommentView.as_view(), name='delete_comment'),
    path('race/<int:race_id>/registration/<int:registration_id>/delete/admin', DeleteRacerFromRegistrationView.as_view(), name='delete_racer_from_registration'),
    path('race/<int:race_id>/result/<int:result_id>/delete/admin', DeleteRacerFromRaceResultView.as_view(), name='delete_racer_from_result'),
    path('race/<int:pk>/edit/admin', EditRaceView.as_view(), name='edit_race'),
    path('race/<int:pk>/delete/admin', DeleteRaceView.as_view(), name='delete_race'),
    path('create_racer_profile/', RacerProfileCreateView.as_view(), name='create_racer_profile'),
    path('profile/<int:pk>/', RacerProfileView.as_view(), name='racer_profile'),
    path('profile/<int:pk>/edit/', RacerProfileUpdateView.as_view(), name='edit_racer_profile'),
]
