from django.urls import path
from alpine_clubs_app import views

urlpatterns = [
    path("cities/", views.CityListView.as_view()),
    path("cities/<int:pk>/", views.CityDetailView.as_view()),
    path("countries/", views.CountryListView.as_view()),
    path("countries/<int:pk>/", views.CountryDetailView.as_view()),
    path("mountains/", views.MountainListView.as_view()),
    path("mountains/<int:pk>/", views.MountainDetailView.as_view()),
    path("routes/", views.RouteListView.as_view()),
    path("routes/<int:pk>/", views.RouteDetailView.as_view()),
    path("ascents/", views.AscentListView.as_view()),
    path("ascents/me/", views.MyAscentParticipationListView.as_view()),
    path("ascents/<int:pk>/", views.AscentDetailView.as_view()),
    path("ascents/<int:pk>/participants/", views.AscentParticipationListView.as_view()),
    path(
        "ascents/<int:ascent_pk>/participants/<int:ascentparticipation_pk>/",
        views.AscentParticipationDetailView.as_view(),  # возможно, имеет смысл поменять ascentparticipation_pk на user_pk
    ),
    path("clubs/", views.ClubListView.as_view()),
    path("clubs/<int:pk>/", views.ClubDetailView.as_view()),
    path(
        "clubs/<int:pk>/members/", views.ClubMembershipListView.as_view()
    ),  # TODO фильтр только на текущих участников
    path(
        "clubs/<int:club_pk>/members/<int:membership_pk>/",
        views.ClubMembershipDetailView.as_view(),
    ),
    path("clubs/<int:pk>/leave/", views.ClubMembershipLeaveView.as_view()),
    path("clubs/me/", views.MyClubMembershipListView.as_view()),
    # TODO возможные пути
    # path("ascents/mountain=",
    # path("routes/mountain=", маршруты определенной горы (в общем, уже есть в делалях горы)
    # просто фильтры, пагинация для list views
]
