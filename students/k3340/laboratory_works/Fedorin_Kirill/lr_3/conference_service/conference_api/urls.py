from django.urls import path, re_path

from .views import ConferenceAPIView, ConferenceDateFilteredAPIView, ConferenceListAPIView, ConferenceUpdateAPIView, OpennedConferencesAPIView

app_name = 'conference_api'

urlpatterns = [
    path('conferences/<int:id>/', ConferenceAPIView.as_view(), name='get_conference'),
    path('conferences/<int:id>/update', ConferenceUpdateAPIView.as_view(), name='update_conference'),
    path('conferences/list/', ConferenceListAPIView.as_view(), name='get_conference_list'),
    path('conferences/free/', OpennedConferencesAPIView.as_view(), name='get_free_conferences'),
    re_path('^conferences/date/(?P<from>\d{4}-\d{2}-\d{2})/(?P<to>\d{4}-\d{2}-\d{2})/$', ConferenceDateFilteredAPIView.as_view(), name='get_conference_by_date')]