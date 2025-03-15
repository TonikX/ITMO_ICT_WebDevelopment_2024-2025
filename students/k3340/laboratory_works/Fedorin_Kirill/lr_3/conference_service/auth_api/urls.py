from django.urls import path, re_path

from .views import (
    ClientsFromTownListAPIView,
    UserAPIView,
    UserConferencesListAPIView,
    UserListAPIView,
    UserParticipationListAPIView,
    UserRelatedReviewersListAPIView,
    UsersRegistrationsListAPIView,
    UserUpdateAPIView,
)

app_name = "auth_api"

urlpatterns = [
    path("users/<int:id>/", UserAPIView.as_view(), name="get_client"),
    #re_path("^users/(?P<id>\d+)/cleaners/(?P<date>\d{4}-\d{2}-\d{2})/$", UserRelatedCleanersListAPIView.as_view(), name="cleaners_by_client"),
    re_path("^users/(?P<id>[0-9]+)/registrations(?:/(?P<from>[0-9]{4}-[0-9]{2}-[0-9]{2}))?(?:/(?P<to>[0-9]{4}-[0-9]{2}-[0-9]{2}))?$", UsersRegistrationsListAPIView.as_view(), name="conferences_by_client"),
    path("users/<int:id>/conferences/", UserConferencesListAPIView.as_view(), name="get_conferences_by_client"),
    path('users/<slug:from_town>/', ClientsFromTownListAPIView.as_view(), name='get_users_from_town'), # TODO: change to getting clients by conference
    path("users/<int:id>/update", UserUpdateAPIView.as_view(), name="update_client"),
    path("users/<int:id>/participation/", UserParticipationListAPIView.as_view(), name="get_participations_by_client"),
    path("users/<int:id>/reviewers/", UserRelatedReviewersListAPIView.as_view(), name="get_reviewers_by_client"),
]