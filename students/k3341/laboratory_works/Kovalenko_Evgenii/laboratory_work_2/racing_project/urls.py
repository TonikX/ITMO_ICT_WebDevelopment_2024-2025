from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from racing_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('races/', views.RaceListView.as_view(), name='race_list'),
    path('races/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('races/<int:race_id>/register/', views.register_for_race, name='race_register'),
    path('races/<int:race_id>/comment/', views.add_comment, name='add_comment'),
    path('racers/', views.RacerListView.as_view(), name='racer_list'),
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.create_racer_profile, name='create_racer_profile'),
    path('admin/race/<int:race_id>/results/', views.race_results_admin, name='race_results_admin'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)