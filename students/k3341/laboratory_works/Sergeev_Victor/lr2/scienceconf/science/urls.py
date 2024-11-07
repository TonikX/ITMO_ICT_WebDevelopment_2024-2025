from django.urls import path
from .views import conference_view, review_view, commentary_view, user_view, speaker_view
urlpatterns = [
    path('', user_view.index),
    path('register/', user_view.RegisterUserView.as_view()),
    path('login/', user_view.LoginUserView.as_view()),
    path('logout/', user_view.UserLogout.as_view()),
    path('conference/', conference_view.ConferenceList.as_view()),
    path('conference/create/', conference_view.ConferenceCreate.as_view()),
    path('conference/<int:pk>/', conference_view.ConferenceDetail.as_view()),
    path('conference/<int:pk>/update/', conference_view.ConferenceUpdate.as_view()),
    path('conference/<int:pk>/delete/', conference_view.ConferenceDelete.as_view()),
    path('conference/<int:pk>/speaker/create/', speaker_view.SpeakerCreate.as_view()),
    path('conference/<int:pk>/speaker/update/', speaker_view.SpeakerUpdate.as_view()),
    path('conference/<int:pk>/speaker/delete/', speaker_view.SpeakerDelete.as_view()),
    path('conference/<int:pk>/auditor/', conference_view.ConferenceAuditor.as_view()),
    path('conference/<int:conf_pk>/review/create/', review_view.ReviewCreate.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/', review_view.ReviewDetail.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/update/', review_view.ReviewUpdate.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/delete/', review_view.ReviewDelete.as_view()),
    path('conference/<int:conf_pk>/review/<int:rev_pk>/comment/create/', commentary_view.CommentCreate.as_view())
]