from django.urls import path
from .views import conference_view, review_view, commentary_view
urlpatterns = [
    path('conference/', conference_view.ConferenceList.as_view()),
    path('conference/<int:pk>/', conference_view.ConferenceDetail.as_view()),
    path('conference/create/', conference_view.ConferenceCreate.as_view()),
    path('conference/<int:pk>/update/', conference_view.ConferenceUpdate.as_view()),
    path('conference/<int:pk>/delete/', conference_view.ConferenceDelete.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/', review_view.ReviewDetail.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/update/', review_view.ReviewUpdate.as_view()),
    path('conference/<int:conf_pk>/review/<int:pk>/delete/', review_view.ReviewDelete.as_view()),
    path('conference/<int:conf_pk>/review/<int:rev_id>/comment/<int:pk>/update', commentary_view.CommentUpdate.as_view()),
    path('conference/<int:conf_pk>/review/<int:rev_id>/comment/<int:pk>/delete', commentary_view.CommentDelete.as_view()),
]