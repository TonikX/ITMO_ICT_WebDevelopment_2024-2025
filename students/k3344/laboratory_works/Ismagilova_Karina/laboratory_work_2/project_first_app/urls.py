from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegistrationView, AllParticipantsListView, ConferenceListView, ConferenceDetailView, \
    MainView, UserDashboardView, AuthorRegistrationView, ParticipantRegistrationView

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('conference/<int:pk>/participant/register/', ParticipantRegistrationView.as_view(), name='participant_registration'),
    path('conference/<int:pk>/author/register/', AuthorRegistrationView.as_view(), name='author_registration'),
    path('participants/', AllParticipantsListView.as_view(), name='all_participants_list'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
]