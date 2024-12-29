from django.urls import path, re_path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('top/', views.top, name='top'),
  re_path(r'^channel/(?P<channel_id>[a-zA-Z0-9_-]{24})/$', views.channel, name='channel'),
  path('channel/add/', views.add_channel, name='add-channel'),
  re_path(r'^add-review/(?P<channel_id>[a-zA-Z0-9_-]{24})/$', views.add_review, name='add-review'),
]