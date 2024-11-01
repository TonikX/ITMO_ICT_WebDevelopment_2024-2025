from django.urls import path
from .views import RaceListView, RaceDetailView, RaceRegistrationView, CommentCreateView, UserRegistrationView, LogoutUser, RacerProfileCreateView, RacerProfileView, RaceUnregisterView, RacerProfileUpdateView, EditRaceView, DeleteRaceView, DeleteCommentView

urlpatterns = [
    path('', RaceListView.as_view(), name='race_list'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('race/<int:pk>/', RaceDetailView.as_view(), name='race_detail'),
    path('race/<int:race_id>/register', RaceRegistrationView.as_view(), name='register_race'),
    path('race/<int:race_id>/unregister', RaceUnregisterView.as_view(), name='unregister_race'),
    path('race/<int:race_id>/comment', CommentCreateView.as_view(), name='add_comment'),
    path('accounts/logout/', LogoutUser.as_view(), name='logout'),
    path('create_racer_profile/', RacerProfileCreateView.as_view(), name='create_racer_profile'),
    path('profile/<int:pk>/', RacerProfileView.as_view(), name='racer_profile'),
    path('profile/<int:pk>/edit/', RacerProfileUpdateView.as_view(), name='edit_racer_profile'),
    path('race/<int:pk>/edit/', EditRaceView.as_view(), name='edit_race'),
    path('race/<int:pk>/delete/', DeleteRaceView.as_view(), name='delete_race'),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment'),
]
