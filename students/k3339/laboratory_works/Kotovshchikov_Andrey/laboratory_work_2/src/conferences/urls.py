from django.urls import path

from conferences import views

urlpatterns = [
    path(
        "",
        views.ConferenceListView.as_view(),
        name="conference-list",
    ),
    path(
        "<int:conference_pk>/",
        views.ConferenceDetailView.as_view(),
        name="conference-detail",
    ),
    path(
        "<int:conference_pk>/delete/",
        views.ConferenceDeleteView.as_view(),
        name="conference-delete",
    ),
    path(
        "<int:conference_pk>/feedback/",
        views.FeedbackView.as_view(),
        name="feedback",
    ),
    path(
        "<int:conference_pk>/invite/",
        views.MemberInvitationView.as_view(),
        name="member-invitation",
    ),
    path(
        "register/",
        views.ConferenceRegistrationView.as_view(),
        name="conference-registration",
    ),
]
