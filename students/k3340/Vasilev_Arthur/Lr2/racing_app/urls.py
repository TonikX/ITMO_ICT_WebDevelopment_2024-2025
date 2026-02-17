from django.urls import path
from . import views

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('race/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('race/<int:pk>/register/', views.RaceRegistrationCreateView.as_view(), name='race_register'),
    path('registration/<int:pk>/update/', views.RaceRegistrationUpdateView.as_view(), name='registration_update'),
    path('registration/<int:pk>/delete/', views.RaceRegistrationDeleteView.as_view(), name='registration_delete'),
    path('race/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('my-registrations/', views.user_registrations, name='user_registrations'),
]