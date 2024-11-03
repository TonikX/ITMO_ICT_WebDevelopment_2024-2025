from django.urls import path
from .views import conference_view
urlpatterns = [
    path('conference/', conference_view.ConferenceList.as_view()),
    path('conference/<int:pk>/', conference_view.ConferenceDetail.as_view()),
    path('conference/create/', conference_view.ConferenceCreate.as_view()),
    path('conference/<int:pk>/update/', conference_view.ConferenceUpdate.as_view()),
    path('conference/<int:pk>/delete/', conference_view.ConferenceDelete.as_view())
]