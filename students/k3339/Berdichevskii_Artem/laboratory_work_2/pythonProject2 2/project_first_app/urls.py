from django.urls import path
from .views import (
    RegisterView,
    AddReviewView,
    ParticipantListView,
    ConferenceDetailView,
    DeleteConferenceView,
    EditConferenceView,
    NewConferenceView,
    HomeView,
    ParticipantDetailView,
    ReviewListView,
    AuthorRegistrationView,
    ParticipantUpdateView,
    ParticipantDeleteView,
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='project_first_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('add_review/<int:conference_id>/', AddReviewView.as_view(), name='add_review'),
    path('conference/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('conference/new/', NewConferenceView.as_view(), name='new_conference'),
    path('conference/<int:pk>/edit/', EditConferenceView.as_view(), name='edit_conference'),
    path('conference/<int:pk>/delete/', DeleteConferenceView.as_view(), name='delete_conference'),
    path('participant/<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('participants/', ParticipantListView.as_view(), name='participant-list'),
    path('author-registration/', AuthorRegistrationView.as_view(), name='author-registration'),
    path('participant/<int:pk>/edit/', ParticipantUpdateView.as_view(), name='edit_participant'),
    path('delete-participant/<int:pk>/', ParticipantDeleteView.as_view(), name='delete_participant'),
    path('accounts/profile/', HomeView.as_view(), name='home'),  # Главная страница
]
