from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import index, RegisterView, AccountDetailsView, logout_view, ConferenceListView, ConferenceDetailView, \
    SpeakerCreateView, RegistrationCreateView, RegistrationListView, SpeakerListView, RegistrationDeleteView, \
    ReviewCreateView

urlpatterns = [
    path('', index),

    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('conferences/<int:pk>/register/', RegistrationCreateView.as_view(), name='conference_create_registration'),
    path('conferences/<int:pk>/propose/', SpeakerCreateView.as_view(), name='conference_propose_speach'),
    path('registrations/', RegistrationListView.as_view(), name='registrations'),
    path('registrations/<int:pk>/cancel/', RegistrationDeleteView.as_view(), name='cancel_registration'),
    path('registrations/<int:pk>/comment/', ReviewCreateView.as_view(), name='comment_conference'),
    path('performances/', SpeakerListView.as_view(), name='performances'),

    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', AccountDetailsView.as_view(), name='account-details'),

    path("admin/", admin.site.urls),
]
